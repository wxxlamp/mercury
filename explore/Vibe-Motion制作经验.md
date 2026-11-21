# Vibe Motion · 让口播、代码动作和声音共同解释一件事

猫学长第 06 集把分镜和调度交给 Codex，执行者分别备料、写代码、渲染。作者自己指出，各镜都能生成，串起来仍可能像幻灯片。他用歌曲的段落解释原因：开头要引人期待，中段要发展，有些地方要推到高潮，有些地方要放下来。对 Mercury 而言，作者第一次审画面时就值得连续看一遍整段。[第 06 集 00:25–00:49、01:07–01:35](../reference/vibe-motion/series/transcripts/06.txt)

| 制作决策 | 从系列里学到什么 | 下一镜怎么试 |
| --- | --- | --- |
| 写运动 | 第 01 集先将指尖位置画回原片。第 02 集分别解决身体跟随和脚的落点。第 04 集用圆锥调鱼群规则。第 08 集用边界、拉力和破裂条件描述薄膜。 | 提示词写对象、约束和触发事件。先看点线能否正确跟随、交接或聚集，再换成最终外观。[第 01 集 00:59 起](../reference/vibe-motion/series/transcripts/01.txt) · [第 08 集 00:26 起](../reference/vibe-motion/series/transcripts/08.txt) |
| 选参考和模型 | 第 03 集分步提交能运行的版本，第 10 集从动作匹配的代码替换内容。第 05、07、09 集展示不同对照办法，第 14 集用具体样题展示工具表现。 | 有合适源码就先换一组本期文字或图形，检查机位仍跟得上；新 skill 用同一模型、同一段预演做比较。导演决定需要什么表现，Sol 执行参数替换。[第 07 集 02:36 起](../reference/vibe-motion/series/transcripts/07.txt) · [第 10 集 00:22 起](../reference/vibe-motion/series/transcripts/10.txt) |
| 写情绪和揭示 | 第 15 集把信息论开头制造预期与反差的做法迁移到蝴蝶效应，再比较同一构思的多种色彩。第 11 集 MV 可观察道具怎样交代人物关系，第 12 集可用画面字幕追踪同一编号。 | 给开场写一句“观众以为接下来会发生什么”，下一镜安排可见的转折。生活片可以靠行李箱和人物反应，技术片可以靠一项意外结果。[第 15 集 00:45–01:27](../reference/vibe-motion/series/transcripts/15.txt) · [第 11、12 集画面观察](../reference/vibe-motion/series/后半观察.md) |
| 设计声音 | 第 13 集用动画帧对齐卡片弹出，又拿同一段 7 秒画面只换选声方案做盲听。真实手电筒开关在 UI 场景里输给了专门设计的点击声。 | 程序把落点对齐，作者连旁白一起听材质与轻重。需找素材、精确合成、调整人声与背景比例时，分别取完整版中的检索、程序音频、混音技能。[第 13 集 00:40、02:40 起](../reference/vibe-motion/series/transcripts/13.txt) · [声音完整版](../reference/vibe-motion/github/sound/README.md) |

**从课程转成自己的制作顺序。** 配套课程从现成录音出发。11:38 把音频转成 SRT，19:11 讨论主讲和补充画面，24:23 讲留白，30:50 把画面指示放在相关台词旁。Mercury 先按文稿和触发词审静音分镜；等你认可视觉方案，再用你的参考音色生成口播，以实际录音校对字幕和动作。导演提示单独保存，干净字幕供观众阅读。[课程章节](../reference/vibe-motion/course/课程简介与章节.txt) · [飞书示例笔记](../reference/vibe-motion/course/阅读入口.md)

**按镜头选实现。** 连续机制图可用组织里 Bingo 的 Remotion 讲解组件，网页细节聚焦可查 fisheye-motion。auto-motion 提供按字幕语义拆段和分镜执行的实例。归档包含前十五集的带时间码转写；第 11 集以歌曲为主，第 12 集的可用文字来自画面字幕，两集的画面观察单独注明。[代码讲解技能](../reference/vibe-motion/github/remotion-code-motion-explainer/SKILL.md) · [技能目录](../reference/vibe-motion/github/目录.md) · [前十五集逐集索引](../reference/vibe-motion/series/transcripts/README.md)
