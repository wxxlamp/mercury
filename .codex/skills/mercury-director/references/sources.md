# 按本片的问题查原件

先定位本片确实要解决的一个问题，选下面对应的材料。如果作者指定了参考，优先打开指定作品。下表路径从 **Mercury 仓库根目录** 起算。在单片工作目录中，`reference/` 专指该片新增的参考；两者分开记录。作者已经提供的本地视频优先直接读取。

| 什么时候打开 | 原件及定位 | 读完怎样改变本片 |
| --- | --- | --- |
| 想把作者的经验变成项目专用 skill | `reference/sources/cangjie-skill/methodology/03-stage1.5-triple-verify.md`。先定位来源，再核查动作可执行性和任务收益。 | 在本片记“原文件与时码、作者讲解、可见变化、迁移的动作、失效条件、验收镜号”。换本片的一组输入做短预演，把结果记入本片 `skills/`。 |
| 多个技术概念割裂，需要决定何时从示意切到实证 | `reference/sources/nginx/BV1cKxf6eEnG.mp4`。00:39–00:50 从全局路线收进一台网店服务器；07:53 拓扑退后，终端和等待计数在前景；15:44 回到请求全程。 | 画出本片的主对象，标明它在切去证据前的位置，以及退回示意后由谁接手。片中的数字用于理解该片实验，本片的论断要绑定自己的证据。 |
| 一句旁白只有文字入场，要找到动作与跨镜交接 | `reference/sources/Table-VideoSOP/official-promo.mp4` 的 00:10–00:12，对照 `reference/sources/Table-VideoSOP/skills/table-video/assets/templates/镜头剧本.template.md`。需诊断成片动作时读同一 skill 下的 `references/motion-check-method.md`。 | 找动作的发起者、接收者、移动对象及交接后的新状态。充分读字的停顿和物件尚未移动的空等分开判断。 |
| 运动漂亮但讲不清过程，或段落像幻灯片 | `reference/vibe-motion/series/transcripts/README.md` 可按集号查转写；第 01 集 00:59 起把轨迹画回原片，第 06 集 01:07 起讲段落目的，第 15 集 00:45 起讲预期与反差。原片从 `reference/vibe-motion/series/README.md` 定位。 | 先用本片点线验证跟随或交接，再写哪一拍建立期待、哪一拍揭示。要复现具体运镜，再打开 MP4 看连续动作。 |
| 希望复用可编辑代码、绑定音效或调用完整版工具 | 查 `reference/vibe-motion/github/remotion-code-motion-explainer/references/reference-reconstruction.md` 与该包 `assets/shot-library/`；声音查 `reference/vibe-motion/github/sound/README.md`，按检索、合成、混音选对应的 SKILL。第 13 集 02:40 起有同一画面的盲听比较。 | 先判断镜头的空间和事件是否匹配，再用本期文字或素材检验代码。特定库的检索、音源和插件按其实际依赖执行，取得素材随本片登记。 |
| 有多版图或作者指出局部问题 | 查 `reference/sources/openfilm/packages/openfilm/manual/film/SKILL.md` 的时间与区域定位，以及 `reference/sources/openfilm/packages/openfilm/plugins/canvas/skills/canvas/SKILL.md` 的分镜组织。 | 带上采用版、镜号、全片秒点和区域。要用 OpenFilm Studio 做交互批注时，使用实际可用的 Studio。 |

**怎样拆一段新参考。** 连播动作发生前、发生时和落点之后，记下构图、视线、对象身份、运动方向、停顿及声音落点。教程有口述时对照同段转写，把作者明确讲的和自己从画面推断的分开。需要贴近原片时固定几帧，按相同画幅对照起止位置、遮挡、曲线和持续时间。记录节拍可迁移之处、需要本片素材替换之处、一条可以在静音预演里验证的问题。

**怎样处理缺件。** 便携环境可以用包内手册起草和排演；对标的原片、指定素材或工具缺失时，在本片分镜旁记下具体缺项。先完成其他可独立判断的镜头，保留该镜的对标或试听状态。逐帧复刻需要原视频，源码复用需要实际源码，听感需可播放的音频。资料索引和文字转述都不足以证明这些工作已经完成。
