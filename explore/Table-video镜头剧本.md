# Table-video · 从一段口播写出能交接的镜头剧本

一只桌子的 42 秒宣传片用同一句话“把任务交给子 Agent”做了对照。00:10 时任务块正在跨过两个工作区的边界，00:12 时它已经停在子 Agent 一侧。即使遮住字幕，观众仍然能看见谁接走了任务。00:25 再用胶片串起制作阶段，让人明白接下来怎样完成整期。[本地样片](../reference/sources/Table-VideoSOP/official-promo.mp4) · [九帧对照](../reference/sources/Table-VideoSOP/table-promo-frames.jpg)

## 从大段到镜头

| 先回答的问题 | 交给下一步什么 |
| --- | --- |
| 观众听完这段要多理解什么？ | 围绕一次变化合并相邻台词。先在大段表写下理解目标，以及下一段为什么接得上。[规划说明](../reference/sources/Table-VideoSOP/skills/table-video/references/planning.md) |
| 这个变化怎么被看见？ | 镜头剧本并排放口播原句和观众看得见的动作。写明起始构图、谁触发什么、视线跟谁走、哪一刻需要停下读字、什么状态交给下一镜。开拍前只有文稿就标触发词；有实际录音再补对齐时间。[镜头剧本模板](../reference/sources/Table-VideoSOP/skills/table-video/assets/templates/镜头剧本.template.md) |
| 多人制作时怎样接得上？ | 总控维护采用版本和全片状态。每位执行者领一个连续段落，带走上一镜结束状态、已选素材和下一镜需要的起点。完成后交可播放片段，一倍速检查交接。[分段开工提示](../reference/sources/Table-VideoSOP/prompts/05_并行准备与分段开工.md) |
| 什么变化需要重新审？ | 改字幕字体就看遮挡与安全区；改配音停顿就重校动作、字幕、音效和接点；改主动作或揭示顺序则返回分镜。作者的意见写在采用版旁，记录实际复查区间。[返修范围](../reference/sources/Table-VideoSOP/skills/table-video/references/review-and-repair.md) |

**给 Mercury 的镜头示例。** 台词是“任务交出去了，但主对话还在继续”。先固定两个工作区，让带标识的任务块从主区移动到子区；任务落下时子区开始处理，镜头拉回，观众看到主区同时接上下一句。审稿图旁就问“能否同时看懂任务归属和主区继续工作？”这样一次审阅可以决定是否采用；材质、曲线和落地音留到动态预演中判断。

上游有九组阶段提示词和完整模板。Mercury 优先融合大段表、镜头剧本和返修方法；每集实际需要的字段放在同一套镜号下。需要新的“接收、处理、返回”动作时再查代码实例。[Table-video 技能](../reference/sources/Table-VideoSOP/skills/table-video/SKILL.md) · [动作源码](../reference/sources/Table-VideoSOP/skills/table-video/assets/motion/)
