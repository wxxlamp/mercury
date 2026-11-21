# 交审、返修与成片交付

从 Mercury 根目录使用仓库的 Python 3.11 环境。以下 $P 表示建档命令返回的单片目录，每个文件参数都相对于本片。导演负责写文稿、制作镜头并交审。只有作者确认了所交版本，才运行对应的 approve，将实际回复写入 --note。

| 何时 | 命令（前缀均为 `.venv/bin/python src/film-review.py "$P"`） |
| --- | --- |
| 优化稿写好 | `submit manuscript manuscript/script-v1.md`，另有证据备注可追加 `--input manuscript/notes-v1.md` |
| 作者确认该稿 | `approve manuscript manuscript/script-v1.md --note "作者的确认意见"` |
| 静音预演和审片材料齐备 | `submit storyboard storyboard/board-v1.md --silent review/board-v1/silent.mp4`，用可重复的 `--input` 附上采用的素材、缩略图、起止帧、参考对照以及本片镜头源代码 |
| 作者确认画面 | `approve storyboard storyboard/board-v1.md --note "作者的确认意见"` |
| 已完成试读、全长口播和带声预演 | `submit preview review/mix-v1/render.json`。从同目录凭据自动取得带声预演、时间线、字幕、干声、分轨、镜头文件和渲染器的指纹。通过 `--input` 补充生成镜头所用的片内源码、素材与依赖清单 |
| 作者确认该带声版本 | `approve preview review/mix-v1/preview.mp4 --note "作者的确认意见"` |
| 终审后渲染并导出 | `export`。在 `exports/mix-v1/` 交付 final.mp4、干声、SRT、manifest.json 及含可重渲输入的 project/，并更新本片 project.json |

文件均用独立版本名。分镜确认之前依靠台词锚点和估时；画面通过后，使用[配音入口](film-voice.md)先试读再做全稿。导演根据真实录音的节奏重排镜头，在本片 src/ 实现运动、生成连续镜头；两次预演和最终编码使用[媒体入口](film-media.md)。导演预先将必要的共享依赖准备为片内可重现的版本，给 submit 逐项传入本片采用的源码、绘图素材和配置。凭据自动覆盖组片程序实际打开的输入，额外资源由制作方声明。

## 返修与恢复

改变论点、事实或台词含义时执行 `revise manuscript`；修改构图、主动作或揭示先后时执行 `revise storyboard`；调整读音、配乐、节奏或字幕位置时执行 `revise preview`。命令清除该层及下游当前批准，历史决定保存在 reviewHistory。继续制作时另存新版，再从受影响的一层交审。已有录音可按句复用。作者只评论某处时，先记录反馈，保留当前采用版直至决定修改。

换会话后，从本片 project.json 的 stage、files、candidates 和 approvals 恢复。旧项目若只有文件名和批准文字，先找对应版本供作者核对，再用上述命令记录指纹。导出前会复查冻结输入。若其内容已变，在对应阶段另存、重新交审。需要在交付副本中重渲时，使用 manifest.json 中 renderer 指定的程序，项目参数传同目录的 project/，时间线取 manifest.json 的 timeline，输出取 project/exports/ 内的新文件名。
