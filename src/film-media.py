"""Assemble project-local, frame-counted shots for a Mercury review."""
import argparse
import hashlib
import json
import math
import os
import shutil
import re
import subprocess
from pathlib import Path
from tempfile import TemporaryDirectory


def sha256(path):
    with path.open("rb") as source:
        return hashlib.file_digest(source, "sha256").hexdigest()


def local_file(root, name):
    if not isinstance(name, str) or Path(name).is_absolute():
        raise ValueError(f"需要片内相对文件路径，收到 {name!r}")
    path = (root / name).resolve(strict=True)
    if not path.is_relative_to(root) or not path.is_file():
        raise ValueError(f"片内文件不存在或路径越界：{name}")
    return path


def ffmpeg(*args):
    subprocess.run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-nostdin",
                    "-xerror", *args], check=True)


def stream(path, selector):
    probe = subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", selector, "-show_streams",
        "-show_format", "-of", "json", path,
    ])
    info = json.loads(probe)
    if not info["streams"]:
        raise ValueError(f"{path} 缺少 {selector} 轨")
    track = info["streams"][0]
    return track, track.get("duration") or info["format"].get("duration")


def seconds(value, label):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value < 0:
        raise ValueError(f"{label} 需要非负秒数，收到 {value!r}")
    return value


def integer(value, label):
    if type(value) is not int or value <= 0:
        raise ValueError(f"{label} 需要正整数")
    return value


def check_subtitles(path, duration):
    def milliseconds(stamp):
        h, m, s, ms = map(int, re.split("[:,]", stamp))
        return ((h * 60 + m) * 60 + s) * 1000 + ms

    text = path.read_text(encoding="utf-8-sig").strip()
    timestamp = r"(\d{2,}:\d{2}:\d{2},\d{3})"
    for cue in re.split(r"\n\s*\n", text):
        lines = cue.splitlines()
        timing = re.fullmatch(timestamp + r"\s*-->\s*" + timestamp, lines[1]) if len(lines) >= 3 else None
        if not timing or not lines[0].strip().isdigit() or not "".join(lines[2:]).strip():
            raise ValueError(f"无法读取 UTF-8 SRT 字幕块：{cue[:100]}")
        begin, end = map(milliseconds, timing.groups())
        if not begin < end <= math.ceil(duration * 1000):
            raise ValueError(f"字幕时间越过画面或顺序错误：{lines[1]}")


def dimensions(size, draft):
    width, height = (integer(n, "size") for n in size)
    if width % 2 or height % 2:
        raise ValueError("H.264 输出画幅宽高须为偶数")
    if draft:
        factor = min(1, 960 / max(width, height))
        return tuple(max(2, round(n * factor / 2) * 2) for n in (width, height))
    return width, height


def prepare_shots(shots, size, fps, load, work, draft):
    width, height = dimensions(size, draft)
    inputs = []
    total_frames = 0
    for index, shot in enumerate(shots):
        source = load(shot["video"])
        frames = integer(shot["frames"], "shot.frames")
        start = seconds(shot.get("start", 0), "shot.start")
        name = f"shot-{index:06d}.mp4"
        # Normalize one shot at a time to bound decoder memory on long films.
        ffmpeg("-ss", str(start), "-i", source, "-map", "0:v:0", "-an", "-sn", "-dn",
               "-vf", f"fps={fps},scale={width}:{height}:force_original_aspect_ratio=decrease,"
                      f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,setsar=1,format=yuv420p",
               "-frames:v", str(frames), "-c:v", "libx264", "-preset", "veryfast" if draft else "medium",
               "-crf", "25" if draft else "17", work / name)
        track, _ = stream(work / name, "v:0")
        if int(track["nb_frames"]) != frames:
            raise ValueError(f"{source.name} 从 {start}s 起不足 {frames} 帧。请校正时间线或延长镜头。")
        inputs.extend([f"file {name}", f"duration {frames / fps:.9f}"])
        total_frames += frames
    if not total_frames:
        raise ValueError("时间线至少需要一个已渲染镜头")
    concat = work / "shots.ffconcat"
    concat.write_text("\n".join(["ffconcat version 1.0", *inputs, ""]), encoding="ascii")
    return concat, total_frames


def audio_mix(timeline, duration, load):
    inputs, filters, labels = [], [], []
    for index, spec in enumerate([{"file": timeline["narration"]}, *timeline.get("tracks", [])], 1):
        path = load(spec["file"])
        _, measured = stream(path, "a:0")
        available = float(measured)
        start = seconds(spec.get("start", 0), "track.start")
        offset = seconds(spec.get("offset", 0), "track.offset")
        length = seconds(spec.get("duration", available - offset), "track.duration")
        gain = spec.get("gainDb", 0)
        if not isinstance(gain, (int, float)) or not math.isfinite(gain):
            raise ValueError("gainDb 需要有限的分贝数")
        if not length or offset + length > available + 0.0005 or start + length > duration + 0.0005:
            raise ValueError(f"{path.name} 音频区间超出素材或画面，请校正镜头或明确裁切该轨。")
        inputs.extend(["-i", path])
        label = f"a{index}"
        filters.append(f"[{index}:a:0]atrim=start={offset}:duration={length},asetpts=PTS-STARTPTS,"
                       f"aresample=48000,aformat=channel_layouts=stereo,volume={gain}dB,"
                       f"adelay={round(start * 48000)}S:all=1[{label}]")
        labels.append(f"[{label}]")
    filters.append("".join(labels) + f"amix=inputs={len(labels)}:normalize=0:duration=longest,"
                   f"apad,atrim=duration={duration}[mix]")
    return inputs, ";".join(filters), len(labels)


def check_hashes(root, inputs):
    for name, digest in inputs.items():
        if sha256(local_file(root, name)) != digest:
            raise ValueError(f"采用版本已发生变化：{name}")


def approved_receipt(root, approval, timeline_name):
    file = approval["file"]
    preview = local_file(root, file)
    if preview.parent.parent != root / "review" or preview.name != "preview.mp4":
        raise ValueError("终审记录必须指向 review/<版本>/preview.mp4")
    receipt_path = preview.parent / "render.json"
    renderer = preview.parent / "film-media.py"
    hashes = approval["inputs"]
    check_hashes(root, hashes)
    receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
    if (receipt["timeline"] != timeline_name or timeline_name not in receipt["inputs"]
            or hashes.get(str(receipt_path.relative_to(root))) != sha256(receipt_path)
            or hashes.get(file) != receipt["preview"]
            or hashes.get(str(renderer.relative_to(root))) != receipt["rendererSha256"]
            or sha256(Path(__file__)) != receipt["rendererSha256"]
            or any(hashes.get(name) != digest for name, digest in receipt["inputs"].items())):
        raise ValueError("终审版本与渲染凭据、时间线或渲染器不符")
    return receipt


def render(project, timeline_name, mode, target):
    root = project.resolve(strict=True)
    state_path = local_file(root, "project.json")
    approvals = json.loads(state_path.read_text(encoding="utf-8"))["approvals"]
    silent, master = mode == "silent", mode == "master"
    stages = ["manuscript"]
    if not silent:
        stages.append("storyboard")
    if master:
        stages.append("preview")
    for stage in stages:
        decision = approvals.get(stage)
        if not decision:
            raise ValueError(f"请先记录作者对 {stage} 的批准")
        check_hashes(root, decision.get("inputs", {}))

    receipt = None
    if master:
        receipt = approved_receipt(root, approvals["preview"], timeline_name)
        output = (root / target).resolve()
        if not output.is_relative_to(root / "exports") or output.suffix.lower() != ".mp4":
            raise ValueError("母版输出路径应在本片 exports/ 下，扩展名为 .mp4")
    else:
        if not re.fullmatch(r"[\w-][\w. -]*", target) or target.endswith((".", " ")):
            raise ValueError("版本名应为单一目录名，以文字、数字、下划线或连字符开头")
        review = root / "review"
        if review.is_symlink() or not review.is_dir():
            raise ValueError("需要本片实际存在的 review/ 目录")
        output = review / target
    if output.exists():
        raise ValueError(f"此版本已存在，请选新版本名：{output}")

    identities = {}

    def load(name):
        path = local_file(root, name)
        if name not in identities:
            identities[name] = sha256(path)
        return path

    timeline_path = load(timeline_name)
    timeline = json.loads(timeline_path.read_text(encoding="utf-8"))
    fps = integer(timeline["fps"], "fps")
    with TemporaryDirectory(dir=output.parent, prefix=".render-") as scratch:
        work = Path(scratch)
        result = work / "result"
        result.mkdir()
        concat, frames = prepare_shots(timeline["shots"], timeline["size"], fps, load, work, not master)
        duration = frames / fps
        args = ["-f", "concat", "-safe", "1", "-i", concat]
        mapping = ["-map", "0:v:0", "-c:v", "copy"]
        subtitle_index = 1
        if not silent:
            inputs, filters, count = audio_mix(timeline, duration, load)
            args.extend(inputs)
            mapping.extend(["-filter_complex", filters, "-map", "[mix]", "-c:a", "aac", "-b:a", "192k"])
            subtitle_index += count
        srt = load(timeline["subtitles"])
        check_subtitles(srt, duration)
        args.extend(["-f", "srt", "-i", srt])
        mapping.extend(["-map", f"{subtitle_index}:s:0", "-c:s", "mov_text",
                        "-metadata:s:s:0", "language=zho", "-disposition:s:0", "default+forced"])
        movie = result / f"{mode}.mp4"
        ffmpeg(*args, *mapping, "-movflags", "+faststart", movie)
        check_hashes(root, identities)
        current = json.loads(state_path.read_text(encoding="utf-8"))["approvals"]
        if any(current.get(stage) != approvals[stage] for stage in stages):
            raise ValueError("制作期间采用版本发生变化，请按本片当前审批重新预演。")
        if mode == "preview":
            snapshot = result / "film-media.py"
            shutil.copyfile(__file__, snapshot)
            built = {"timeline": timeline_name, "inputs": identities,
                     "rendererSha256": sha256(snapshot), "preview": sha256(movie)}
            (result / "render.json").write_text(json.dumps(built, ensure_ascii=False, indent=2) + "\n",
                                                encoding="utf-8")
        if master:
            if identities != receipt["inputs"]:
                raise ValueError("母版实际使用的输入与终审凭据不符")
            os.link(movie, output)
        else:
            result.rename(output)
    print(output.relative_to(root))


if __name__ == "__main__":
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("project", type=Path)
    cli.add_argument("timeline", help="片内时间线 JSON 路径")
    cli.add_argument("mode", choices=["silent", "preview", "master"])
    cli.add_argument("target", help="review/ 下的新版本名，或 master 模式的 exports/ 内目标 MP4")
    options = cli.parse_args()
    try:
        render(options.project, options.timeline, options.mode, options.target)
    except (OSError, ValueError, KeyError, TypeError, subprocess.SubprocessError) as error:
        cli.exit(1, f"制作失败：{error}\n")
