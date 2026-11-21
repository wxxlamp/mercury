# 用单片时间线组装预演

在仓库根目录运行。先在本片 `src/` 做镜头动画，并将每段渲染为可单独解码的视频。组装器保留这些片段里的构图、运动和转场。跨镜转场可在相邻片段中预渲。准备 UTF-8 SRT 供静音时读词。

```sh
.venv/bin/python src/film-media.py "projects/片名" src/timeline-silent-v1.json silent 分镜-v1
.venv/bin/python src/film-media.py "projects/片名" src/timeline-voiced-v1.json preview 带声-v1
```

时间线使用本片相对路径。例如一段两秒镜头和一段三秒镜头，用下列数据组装。

```json
{
  "size": [1920, 1080],
  "fps": 30,
  "shots": [
    {"video": "src/M01-v1.mp4", "frames": 60},
    {"video": "src/M02-v2.mp4", "start": 0.5, "frames": 90}
  ],
  "subtitles": "audio/已审稿-v2.srt",
  "narration": "audio/旁白-v2.wav",
  "tracks": [
    {"file": "assets/抵达.wav", "start": 2.2, "gainDb": -8},
    {"file": "audio/音乐-v1.wav", "start": 0, "offset": 1, "duration": 5, "gainDb": -19}
  ]
}
```

- `size` 是成片的偶数像素宽高，`fps` 为正整数。输入画幅不同时等比留边。每镜 `start` 是素材内起点秒数，`frames` 是按成片帧率取用的帧数。镜头需要足够长，补画或调整停顿后另存新版。
- 文稿获批后运行 `silent`。把估时字幕存入 `storyboard/`，在该版时间线用 `subtitles` 引用。此阶段只需 `size`、`fps`、`shots`、`subtitles`。结果是 `review/分镜-v1/silent.mp4`。字幕为 MP4 内的默认、强制显示中文轨。请用支持 mov_text 的播放器回看，例如 QuickTime Player，若字幕隐藏，手动开启中文字幕。中文字体及字幕样式由播放器提供。
- 静音分镜获批后，根据实录调整镜头帧数和字幕时间。运行 `preview` 时必须提供全长干声，终审用该版干净 SRT。每条可选音乐或拟音的 `start` 是全片起点，`offset` 与 `duration` 是从素材取用的秒数，`gainDb` 是混音前增益。需要随旁白压音乐时，将已做好音量包络的音乐分轨传入。只有在画面明确有留白时让旁白早于画面结束。音频或字幕超过画面会报错。
- 带声模式在 `review/带声-v1/` 写入全长低清 `preview.mp4`、`render.json` 和渲染器快照 `film-media.py`。预演长边最多 960 像素。凭据记录时间线与实际读取的媒体路径、输入文件和渲染器的 SHA-256、预演的 SHA-256。提交终审时同时绑定制作这些镜头的片内源码和上游素材。作者批准该预演后，交付程序调用这份快照，以相同剪辑与混音按原画幅生成母版。
- 重渲已交付版本时，在交付包的 `project/` 根目录运行 `python3 review/带声-v1/film-media.py . src/timeline-voiced-v1.json master exports/重渲.mp4`，把示例路径换成冻结清单中的实际路径。工具核对终审、素材、时间线及渲染器的摘要。
- 每次换用新版本名。该命令使用 PATH 上的 ffmpeg、ffprobe 和 FFmpeg 的 H.264、AAC、mov_text 编码器。临时渲染完成后才出现完整的版本目录。
