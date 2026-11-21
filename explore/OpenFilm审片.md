# OpenFilm · 让作者能指着画面提修改

OpenFilm 把备选素材放在画板，用时间线记录实际采用的镜头，还能把批注定位到某一秒的某个画面区域。Mercury 可以先借用这套审片方式，在 Remotion 工程中用镜号和时间定位；需要交互式剪辑时再接入 OpenFilm。[工具入口](../reference/sources/openfilm/skills/openfilm/SKILL.md) · [工程格式](../reference/sources/openfilm/packages/openfilm/SPEC.md)

| 制作时刻 | OpenFilm 怎样做 | Mercury 怎样用 |
| --- | --- | --- |
| 审分镜 | Canvas 把一镜的意图、参考图和动态候选放在同一行；多个镜头可共同引用一张人物参考。选中的镜头再进入时间线。 | 每行放这一段原话、关键帧和动态草图。给生活片选定人物照片或道具后，在相关镜头里复用这份参照。[画板说明](../reference/sources/openfilm/packages/openfilm/plugins/canvas/skills/canvas/SKILL.md) |
| 准备素材 | Media 先查作者已有素材，再查素材库，最后按具体缺口调用外部服务。Color 支持同场景共享校色，也支持单镜调整。 | 本人照片、实拍和原始截图优先；缺少插画才找或生成。混用手机实拍和照片时，连看切点两侧的人脸和白平衡。[媒体选择](../reference/sources/openfilm/packages/openfilm/manual/media/SKILL.md) · [校色说明](../reference/sources/openfilm/packages/openfilm/plugins/color/skills/color/SKILL.md) |
| 回看一个问题 | Film 支持镜头 ID、全片时间范围和画面区域，轨道还能锁定。给定同一时间，代码镜头要能重现同一帧。 | 反馈带上预演版本、镜号、秒点或台词、区域、预期变化。局部重做后，在同一位置检查结果并播放相邻镜头。[时间线与画面定位](../reference/sources/openfilm/packages/openfilm/manual/film/SKILL.md) |

**一条可执行的审片意见。** “预演 v2，第 4 镜，念到‘返回’时，右下角的状态码被字幕挡住了。保留终端位置，让字幕移开，等数字读清再退回全景。”执行者能定位对象、知道哪些关系要保留，也能确定该怎样回看。若从静音稿切换到实际配音版本，用镜号和台词重新定位，秒点随新版更新。

**时间线交接。** OpenFilm 区分素材内的裁切时间与该镜在全片的入点。Mercury 同样区分镜内事件和全片时间。一次点击声绑定镜内的“按钮按下”，剪短前一镜时由时间线带着它一起移动。真实旁白和音乐分轨保存，终审可单听说话、静音看画面，再按一倍速合听。[镜内时间、轨道与声音](../reference/sources/openfilm/packages/openfilm/manual/film/SKILL.md)
