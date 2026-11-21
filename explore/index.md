# 剪辑技巧索引

从当前镜头的问题入手。每行给出一种剪法、可以查阅的本地 skill 或作品目录，以及预演时要判断的问题。采用的原片片段、代码版本和音效记在本片工程。

按已审稿希望观众看完能回答的问题选片型。混合题材可以用一种手法组织整片，在需要举证或回忆的一段借用另一种。

| 观众想弄清什么 | 片型指南 |
| --- | --- |
| 日常现象背后是怎么回事？ | [常识科普：沿一个对象逐步解释](常识科普剪辑.md) |
| 作者为什么这样判断，什么情况会改变结论？ | [话题讨论：对照、证据与反例](话题讨论剪辑.md) |
| 系统里究竟哪一步改变了结果？ | [技术科普：在机制图和真实运行之间切换](技术科普剪辑.md) |
| 当时发生了什么，这个人为什么做出那个选择？ | [个人生活：用动作、旧物和声音串起经历](个人生活剪辑.md) |

## 叙事与分镜

| 遇到的问题 | 可尝试的剪法与验收问题 | 参考入口 |
| --- | --- | --- |
| 概念多，观众记不住主线 | 固定一笔钱、一个请求或一件道具。遇到困难才引入下个角色，结尾沿原路径重走。观众还能指出对象在哪、谁改变了它吗？ | [小盒子童鞋 · 网关科普](../reference/sources/nginx/) |
| 一张全景图有五个角色，观众不知道先看谁 | 开场交代全貌，随后只展开遇到困难的一角。跟着同一对象，每次亮出一个条件，其余保留轮廓或问号。回到全图时，让观众指出谁刚刚接手。 | [小盒子童鞋 · 网关科普](../reference/sources/nginx/) |
| 逐句做动画，连起来像翻页 | 按铺垫、预期、揭示和余韵划段。多句可共用一个动作，揭示前留出观众形成预期的一拍。静音连看时，转折落在哪里？ | [猫学长 · Vibe Motion 合集](../reference/vibe-motion/series/) · [table-video](../reference/sources/Table-VideoSOP/skills/table-video/) |
| “交给”“返回”停留在字幕里 | 画出发起者、对象和接收者，上一镜的结果成为下一镜起点。去掉箭头说明后，观众能看懂谁接手了吗？ | [table-video](../reference/sources/Table-VideoSOP/skills/table-video/) · [代码讲解镜头](../reference/vibe-motion/github/remotion-code-motion-explainer/) |
| 不确定哪里该插截图、哪里让口播继续 | 主讲承载叙述，在证据、机制或情绪发生变化处插入补充镜头。对截图先交代页面，再聚焦目标，读完退回同一对象。 | [猫学长 · 录音与剪辑课程](../reference/vibe-motion/course/) · [fisheye-motion](../reference/vibe-motion/github/skills/fisheye-motion/) |
| 有实验结论，示意图该在哪一拍切到实证？ | 让拓扑退到背景，把本期日志或录屏的输入条件与结果一起留在前景。若结论是“等了很久”，保留计数或时间线索。切回原位置后，观众能解释刚才验证了哪一步吗？ | [小盒子童鞋 · 网关科普](../reference/sources/nginx/) |
| 想借用一段参考的风格 | 拆出开始状态、触发、落点，区分作者口述与画面观察。口述识别失真时标明采用了画面字幕。用本期台词和素材试同一关系，在片内方法卡记下出处、操作、效果和失效条件。哪些已有原片或预演验证，哪些还待作者判断？ | [仓颉 · 方法提取](../reference/sources/cangjie-skill/) · [Vibe Motion 合集](../reference/vibe-motion/series/) |

## 构图、运镜与素材

| 遇到的问题 | 可尝试的剪法与验收问题 | 参考入口 |
| --- | --- | --- |
| 不知道何时推近、何时拉远 | 比较两端关系时固定全景；辨认字段时沿已知对象推近；需要看见后果时拉回。纵深本身有意义时再试视差或绕行。 | [连续空间与代码镜头](../reference/vibe-motion/github/remotion-code-motion-explainer/) · [perspective-illusion](../reference/vibe-motion/github/skills/perspective-illusion/) |
| 角色或图形动作发飘 | 分别看预备、接触、反应、收势。需要复现轨迹时先把采样点画回原片，核对方向和接触位置。用点线或占位形体跑通约束和触发事件，再替换外观。停在接触帧，能指出是谁带动谁吗？ | [迪士尼动画原则](../reference/vibe-motion/github/skills/disney-animation-rule-skill/) · [程序鱼](../reference/vibe-motion/github/procedural-fish/) · [群体运动](../reference/vibe-motion/github/threejs-boids/) |
| 教程需要观众看清输入和反馈 | 先明确输入区域，再让输入发生，保留对应结果供对照。真实操作优先用本片录屏，需要解释输入过程时可用打字动画示意。 | [claude-typer](../reference/vibe-motion/github/skills/claude-typer/) · [OpenFilm Media](../reference/sources/openfilm/packages/openfilm/manual/media/) |
| 本人实拍、网上图片和生成图，该用哪种？ | 先从本片已有的实拍、照片或原始截图里选能支撑这句话的素材，再查共享库，按缺口补拍、检索或生成。补画的场景标为示意，审片时能分清哪些是亲历或实证吗？ | [OpenFilm Media](../reference/sources/openfilm/packages/openfilm/manual/media/) |
| 一个标志或关键词需要逐步显现 | 想让轮廓参与动作时将标志拆成可编辑图层；想控制文字揭示顺序时用扫光。第一次看清对象后，让视线回到主叙事。 | [pixel2motion](../reference/vibe-motion/github/skills/pixel2motion/) · [light-spotlight-render](../reference/vibe-motion/github/skills/light-spotlight-render/) |
| 找到相似动画代码，换了内容机位就跟丢 | 先挑动作关系最接近的一段代码，换成本期的文字或物件，每改一步就渲染代表段。比较两种 skill 时固定模型和输入，逐帧看换字或换形后焦点还能否落准。 | [猫学长 · Vibe Motion 合集](../reference/vibe-motion/series/) · [代码讲解镜头](../reference/vibe-motion/github/remotion-code-motion-explainer/) |
| 生活片混用照片和手机实拍 | 想表达记忆变化时可用一次黑白转彩；跨镜色差分散注意时先匹配曝光和白平衡。连看切点两侧，人和地点是否仍好辨认？ | [colorize](../reference/vibe-motion/github/skills/colorize/) · [OpenFilm Color](../reference/sources/openfilm/packages/openfilm/plugins/color/skills/color/) |
| 需要表现规模、位置或进度 | 让数据决定图形。相对进度可以用刻度；跨地域移动可以用航线；价格区间可用真实 OHLC 数据。观众能读出本句所说的差异吗？ | [刻度进度](../reference/vibe-motion/github/skills/ruler-progress-render/) · [地球航线](../reference/vibe-motion/github/skills/threejs-earth-render/) · [K 线](../reference/vibe-motion/github/skills/remotion-candlestick/) |

## 配音、节奏与声音

| 遇到的问题 | 可尝试的剪法与验收问题 | 参考入口 |
| --- | --- | --- |
| 配音后镜头太赶，停顿被剪没 | 分镜先定触发词。本人音色口播生成后以已审稿核字，按实录的气口和重音定字幕入点。画面指示另记在对应稿段，交付的 SRT 只留口播。让跨句动作保留连续性。查证据或等待反应时给足停留。 | [录音与剪辑课程](../reference/vibe-motion/course/) · [auto-motion](../reference/vibe-motion/github/auto-motion/) |
| 前一镜剪短后，后面的点击声提前了 | 记下接触点在源素材中的时间、素材裁切起点和这一镜在全片的入点。正常速度下，全片响点等于入点加上接触点与裁切起点的差。改速后按新播放速度重算，回听是否仍在按下的一帧响。 | [OpenFilm Film](../reference/sources/openfilm/packages/openfilm/manual/film/) |
| 动作卡点准，听起来仍不贴 | 真实物件按材质找拟音，UI 点击可先试听同套界面音。固定画面、旁白和响度对比候选，检查声音像哪个物件发出来的。 | [sfx-sources](../reference/vibe-motion/github/sound/sfx-sources/) · [猫学长声音案例](../reference/vibe-motion/series/) |
| 提示音要跟随一组动作，或配乐盖住关键词 | 精确音高、包络和节拍可用程序音；保持旁白、音乐、拟音分轨。把音效绑定接触帧，关键句下压音乐，试听尾响是否撞到下一句。 | [procedural-audio](../reference/vibe-motion/github/sound/procedural-audio/) · [audio-mixing](../reference/vibe-motion/github/sound/audio-mixing/) |

## 预演、审片与返修

| 遇到的问题 | 可尝试的剪法与验收问题 | 参考入口 |
| --- | --- | --- |
| 有几版分镜，作者很难比较 | 每段并排放原句、起止关键帧、素材缩略图和动态候选。把本片代表段与选中的参考片段并排，比较动作落点和揭示时机。共用同一人物或物件参照，选中的镜头串起来静音连看。 | [OpenFilm Canvas](../reference/sources/openfilm/packages/openfilm/plugins/canvas/skills/canvas/) · [table-video](../reference/sources/Table-VideoSOP/skills/table-video/) |
| 两人各做好了镜头，拼接时视线和方向断了 | 按连续段落交接。同一镜号下写明上一镜结束状态、本段要揭示的变化、下一镜起点和采用的素材版本。交回可播放片段后，以一倍速连看接点两侧，对象还在同一方向吗？ | [table-video](../reference/sources/Table-VideoSOP/skills/table-video/) |
| 反馈是“这里太快”，不知道该改哪里 | 用预演版本、镜号、秒点、画面区域复现。先判断是揭示太早、运动太快还是读字不够，再改对应镜头。带着前后镜一倍速复查。 | [OpenFilm Film](../reference/sources/openfilm/packages/openfilm/manual/film/) · [table-video](../reference/sources/Table-VideoSOP/skills/table-video/) |
| 改了一处，哪些镜头要重审？ | 改字幕字体就看遮挡和安全区。换气口就重校该段及后续的字幕、动作和拟音。换主动作或揭示顺序则回到分镜。沿用镜号与台词，在新预演重新定位秒点，并记录实际复看的范围。 | [table-video](../reference/sources/Table-VideoSOP/skills/table-video/) · [OpenFilm Film](../reference/sources/openfilm/packages/openfilm/manual/film/) |

要看具体出处和片段分析，可读五份研究笔记：[仓颉](仓颉技能提炼.md)、[Nginx](Nginx网关视频.md)、[OpenFilm](OpenFilm审片.md)、[Table-video](Table-video镜头剧本.md)、[Vibe Motion](Vibe-Motion制作经验.md)。索引收录的是可选技巧。单片试验、效果和意见留在对应项目，结项后由作者 Review 并选择要沉淀的条目。
