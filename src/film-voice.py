"""Build a versioned narration WAV and SRT from approved dialogue and local takes."""

import argparse
import hashlib
import http.client
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import wave
from pathlib import Path

RATE = 48000


def project_file(root, relative):
    if not isinstance(relative, str) or not relative or Path(relative).is_absolute():
        raise ValueError(f"需要片内相对文件路径：{relative!r}")
    path = (root / relative).resolve(strict=True)
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError(f"文件超出本片或不是普通文件：{relative}")
    return path


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def safe_name(name):
    if not isinstance(name, str) or not re.fullmatch(r"[\w-][\w.-]*", name) or name.endswith("."):
        raise ValueError(f"版本名和段号须为独立文件名：{name!r}")
    return name


def timing_option(segment, name):
    value = segment.get(name, 0)
    if type(value) is not int or value < 0:
        raise ValueError(f"{segment['id']} 的 {name} 需要非负整数毫秒")
    return value


def approved_script(root):
    state = read_json(project_file(root, "project.json"))
    if state["stage"] not in ("voice", "review"):
        raise ValueError("须等文稿与静音分镜获批后进入 voice 或 review 阶段")
    approvals = state["approvals"]
    expected = {}
    for key, field in (("manuscript", "script"), ("storyboard", "storyboard")):
        approval = approvals.get(key)
        if not isinstance(approval, dict) or not approval.get("file"):
            raise ValueError(f"缺少作者的 {key} 审阅记录")
        if state["files"].get(field) != approval["file"]:
            raise ValueError(f"{key} 与作者批准的文件不一致")
        project_file(root, approval["file"])
        expected.update(approval.get("inputs", {}))
    for name, fingerprint in expected.items():
        with project_file(root, name).open("rb") as source:
            if hashlib.file_digest(source, "sha256").hexdigest() != fingerprint:
                raise ValueError(f"已审版本的输入发生变化：{name}")
    script = project_file(root, state["files"]["script"])
    return script, approvals["manuscript"], approvals["storyboard"]


def check_dialogue(script, segments):
    if not isinstance(segments, list) or not segments:
        raise ValueError("配音计划需要非空的 segments 数组")
    ids = set()
    for seg in segments:
        name = safe_name(seg["id"])
        if name.casefold() in ids:
            raise ValueError(f"重复的段号：{name}")
        ids.add(name.casefold())
        if not isinstance(seg["text"], str) or not seg["text"].strip() or "\n\n" in seg["text"]:
            raise ValueError(f"{name} 需要一条可朗读的字幕")
    # Accept plain dialogue and stand-alone S01-style paragraph markers.
    lines = script.read_text(encoding="utf-8-sig").splitlines()
    spoken = "".join(line for line in lines if not re.fullmatch(r"\s*(?:#{1,6}\s+)?S\d+\s*", line))
    expected = "".join(spoken.split())
    actual = "".join("".join(seg["text"].split()) for seg in segments)
    if actual != expected:
        raise ValueError("逐条 text 合起后须覆盖整份已审口播，保留原字与标点。证据和审阅意见另存。")


def synthesize(root, segment, reference, port, output):
    if not isinstance(reference, dict) or not reference.get("audio"):
        raise ValueError(f"{segment['id']} 缺少 recording 或 reference.audio")
    ref = project_file(root, reference["audio"])
    speed = reference.get("speed_factor", 1.0)
    if isinstance(speed, bool) or not isinstance(speed, (int, float)) or not math.isfinite(speed) or speed <= 0:
        raise ValueError("reference.speed_factor 需要正数")
    spoken = segment.get("spoken", segment["text"])
    if not isinstance(spoken, str) or not spoken.strip():
        raise ValueError(f"{segment['id']} 的 spoken 需要可朗读的文字")
    payload = {
        "text": spoken, "text_lang": "zh", "ref_audio_path": str(ref),
        "prompt_text": reference.get("text", ""), "prompt_lang": "zh",
        "media_type": "wav", "streaming_mode": False, "speed_factor": speed,
    }
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=240)
    try:
        connection.request("POST", "/tts", json.dumps(payload).encode(), {"Content-Type": "application/json"})
        response = connection.getresponse()
        if response.status != 200:
            details = response.read(384).decode(errors="replace")
            raise ValueError(f"本机 GPT-SoVITS 返回 HTTP {response.status}：{details}")
        with output.open("wb") as audio:
            shutil.copyfileobj(response, audio)
    except (OSError, http.client.HTTPException) as error:
        raise ValueError(f"无法从本机 GPT-SoVITS 取得音频（127.0.0.1:{port}）：{error}") from error
    finally:
        connection.close()


def srt_time(frames):
    millis = (frames * 1000 + RATE // 2) // RATE
    seconds, ms = divmod(millis, 1000)
    minutes, sec = divmod(seconds, 60)
    hours, minute = divmod(minutes, 60)
    return f"{hours:02}:{minute:02}:{sec:02},{ms:03}"


def render(root, plan, selected, output, port):
    clips = output / "segments"
    clips.mkdir()
    captions = []
    cursor = 0
    with wave.open(str(output / "narration.wav"), "wb") as narration:
        narration.setparams((1, 2, RATE, 0, "NONE", "not compressed"))
        for number, seg in enumerate(selected, 1):
            clip = clips / f"{seg['id']}.wav"
            if "recording" in seg:
                source = project_file(root, seg["recording"])
            else:
                source = output / "response.wav"
                synthesize(root, seg, plan.get("reference"), port, source)
            subprocess.run([
                "ffmpeg", "-nostdin", "-v", "error", "-protocol_whitelist", "file,pipe", "-i", str(source), "-map", "0:a:0",
                "-ac", "1", "-ar", str(RATE), "-c:a", "pcm_s16le", str(clip)
            ], check=True)
            if "recording" not in seg:
                source.unlink()
            with wave.open(str(clip), "rb") as take:
                frames = take.getnframes()
                start = cursor + timing_option(seg, "lead_ms") * RATE // 1000
                end = cursor + frames - timing_option(seg, "tail_ms") * RATE // 1000
                if end <= start or srt_time(start) == srt_time(end):
                    raise ValueError(f"{seg['id']} 的可听区间为空，请检查录音及起止")
                captions.append(f"{number}\n{srt_time(start)} --> {srt_time(end)}\n{seg['text'].strip()}\n")
                while chunk := take.readframes(RATE):
                    narration.writeframesraw(chunk)
            cursor += frames
    (output / "subtitles.srt").write_text("\n".join(captions), encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("plan", help="片内配音计划 JSON")
    parser.add_argument("version", help="audio 下的新版本名")
    parser.add_argument("--sample", metavar="ID", help="只生成这句试读")
    parser.add_argument("--port", type=int, default=9880, help="本机 GPT-SoVITS api_v2 端口")
    args = parser.parse_args()
    root = args.project.resolve(strict=True)
    approval = approved_script(root)
    script = approval[0]
    plan = read_json(project_file(root, args.plan))
    segments = plan["segments"]
    check_dialogue(script, segments)
    selected = [seg for seg in segments if seg["id"] == args.sample] if args.sample else segments
    if not selected:
        raise ValueError(f"没有段号 {args.sample}")
    audio = (root / "audio").resolve(strict=True)
    if audio.parent != root or audio.name != "audio":
        raise ValueError("audio 必须是本片的实际目录")
    destination = audio / safe_name(args.version)
    if destination.exists() or destination.is_symlink():
        raise ValueError(f"版本已存在，请另取版本名：{destination.name}")
    with tempfile.TemporaryDirectory(dir=audio, prefix=".voice-") as tmp:
        output = Path(tmp) / "mix"
        output.mkdir()
        render(root, plan, selected, output, args.port)
        if approved_script(root) != approval:
            raise ValueError("配音期间文稿或分镜的采用版有变，请从当前版本重新生成")
        # Publish the complete nonempty directory in one rename on the same file system.
        os.rename(output, destination)
    print(destination)


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, wave.Error, subprocess.CalledProcessError) as error:
        sys.exit(f"配音失败：{error}")
