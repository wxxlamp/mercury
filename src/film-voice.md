# 本人音色试读、干声与字幕

文稿和静音分镜获批后，在本片 `audio/` 保存参考录音、录音的准确文字及配音计划。提供已有逐句录音时可直接生成整条干声。需要合成的句子使用本机 GPT-SoVITS 服务，服务与 Mercury 需要能读取同一份本地参考音频。先在已安装模型的环境启动 `python api_v2.py -a 127.0.0.1 -p 9880`。模型有不同的音色、设备和样本要求，用试读决定采用哪一版。[GPT-SoVITS 作者的 API 定义](https://github.com/RVC-Boss/GPT-SoVITS/blob/main/api_v2.py)

配音计划按实际说话顺序排列，一条字幕对应一句或一个短意群。以下示例中 S01 用参考音色合成，S02 使用已有录音。每条 `text` 连起来要覆盖 `files.script` 的全部口播，程序忽略空白和单独一行的 `S01` 或 `## S01` 段号。证据、标题说明和导演提示放在稿外。若旧版已审稿包含编辑批注，另存纯口播版，由作者核对采用版本后录制。

```json
{
  "reference": {"audio": "audio/voice-reference.wav", "text": "这是我用来试音的一句话。"},
  "segments": [
    {"id": "S01", "text": "请求已经送到了。"},
    {"id": "S02", "text": "回执为什么还没来？", "recording": "audio/takes/S02.wav"}
  ]
}
```

在 Mercury 根目录运行，路径参数均为本片内相对路径，首个项目目录参数除外。

```sh
.venv/bin/python src/film-voice.py "projects/请求去哪了" audio/plan-v1.json trial-v1 --sample S01
.venv/bin/python src/film-voice.py "projects/请求去哪了" audio/plan-v1.json voice-v1
```

可用正数 `reference.speed_factor` 调整试读语速。纠正专名读音时，在对应句的 `spoken` 填写仅供合成的注音式读法，字幕仍采用已审的 `text`。

先试听试读。确定声线、语速和专名读法后，再执行第二条命令。要保留试读的表演，可将该句的 `recording` 指向 `audio/trial-v1/segments/S01.wav`。每次运行写入新的 `audio/<版本>/`，包括归一为 48 kHz 单声道 PCM 格式的逐句 WAV、整条 `narration.wav` 和 `subtitles.srt`。程序只读 `project.json`，检查文稿、分镜审批及当前阶段。导演试听校对后再登记采用版。输出的 SRT 以已审稿核字，以实际录音采样数定位到句。若某句开头有吸气或句尾留有空白，可在该条填写 `lead_ms` 和 `tail_ms`，手动收紧字幕的起止，保留完整干声。逐词卡点需在录音上单独听准并写入本片时间线。

返修某句时另存计划。给已采用的其他句填写原版 `segments/<段号>.wav` 的片内路径，仅让待改句重新合成或引用新录音，输出一个新版本。所有下游时间码将随录音长度重算。检查受影响的接点和字幕，再更新预演。
