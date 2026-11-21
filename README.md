# Mercury

每部视频用独立项目和独立 Codex 会话制作。公共代码在 `src/`，已批准共享的素材在 `assets/`。

## 新建一部片

在 **Mercury 根目录新开 Codex 对话，直接粘贴文稿**。导演会在 `projects/` 下建片、保存原文、另写优化稿，然后在同一对话请你审稿。可附片名；省略时以首行生成临时片名。下次续作时告诉导演原项目名或路径。

已有 Markdown 或文本文件时，也可以运行 `npm run project:new -- "片名" "./原稿.md"`。文稿、静音分镜、带声预演分别等你确认，终审通过后按获批组合渲染并输出到本片 `exports/`。本人音色合成需本人参考录音和已启动的兼容后端。[项目目录](projects/AGENTS.md) · [交审与导出](src/film-review.md) · [配音](src/film-voice.md) · [动态预演](src/film-media.md)

## Codex 配置与迁移

主会话担任导演，可按任务调用 `motion-worker` 和 `reviewer`。公共[导演 skill](.codex/skills/mercury-director/SKILL.md)放在 `.codex/skills/`。已在本机 Codex CLI 0.171.0 的受信任仓库中验证，从片目录可以直接发现它。若其他客户端未列出技能，可按根目录 AGENTS.md 中的路径直接读取。

当前导演 skill 可以直接引用仓库根目录的 [reference/](reference/reference.md)。公共调研中的候选做法留在 `explore/`，单片试验留在本片，等你 Review 并选定条目后再沉淀到公共 skill。需要对标一段具体运镜或节奏时打开参考原片，需要复用代码或运行完整版声音工具时读取相应源码与脚本。[按剪辑技巧查对应 skill 或作品](explore/index.md)。

迁移基本导演方法时携带整个 skill 目录。迁移 Mercury 工程时一并携带 `explore/index.md`、`.codex/`、根与项目层的工作约定、`src/`、`package.json` 和本片文件；需要参考对标或外部工具时同时携带本次使用的原件及依赖。媒体若是指向本机原片的链接，迁移后要确认目标可播放。

[项目需求](requirements.md) · [视频制作工作流](explore/视频制作工作流.md) · [本机研究资料](reference/reference.md)
