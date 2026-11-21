# mercury 本地环境初始化

在 macOS 的 VS Code 中打开仓库根目录。提前安装 [pyenv](https://github.com/pyenv/pyenv#installation)、[nvm](https://github.com/nvm-sh/nvm#installing-and-updating) 以及 Microsoft 的 Python 和 Python Debugger 扩展。以下命令在仓库根目录的 zsh 终端执行。

## Python

[.python-version](.python-version) 将 Python 固定为 **3.11.4**。首次初始化时创建仓库内的 `.venv`，以后新开终端只需重新激活它。

```zsh
eval "$(pyenv init - zsh)"
pyenv install -s "$(cat .python-version)"
python -m venv .venv
source .venv/bin/activate
python --version
```

预期输出为 `Python 3.11.4`。以后如果项目提供 `requirements.txt`，在激活 `.venv` 后运行 `python -m pip install -r requirements.txt`。

[.vscode/settings.json](.vscode/settings.json) 将默认 Python 环境指向 `.venv`。如果 VS Code 缓存了旧解释器，在命令面板运行 `Python: Select Interpreter`，选择仓库内的 `.venv/bin/python`。 [VS Code Python 环境文档](https://code.visualstudio.com/docs/python/environments#_select-an-environment)

## Node.js

[.nvmrc](.nvmrc) 将 Node.js 固定为 **22.22.1**。如果终端已经加载 `nvm`，可从 `nvm install` 开始。版本安装好后，每次新开终端在仓库根目录运行 `nvm use` 即可。

```zsh
export NVM_DIR="${NVM_DIR:-$HOME/.nvm}"
source "$NVM_DIR/nvm.sh"
nvm install
nvm use
node --version
npm --version
```

预期 Node.js 输出为 `v22.22.1`。当前的项目初始化命令仅依赖 Node.js 标准库，见 [README](README.md)。以后项目新增依赖时，有 `package-lock.json` 就用 `npm ci`，首次生成锁文件用 `npm install`。

## 在 VS Code 调试

打开要调试的 `.py` 或 `.js` 文件，在「运行和调试」面板选择 [.vscode/launch.json](.vscode/launch.json) 中的对应配置，再按 `F5`。两者都以仓库根目录为工作目录，并在集成终端中运行。

| 配置 | 运行环境 |
| --- | --- |
| `Python: Debug Current File` | 仓库内的 `.venv/bin/python` |
| `Node: Debug Current File` | nvm 已安装的 Node.js `22.22.1` |

升级 Python 后，用新版本重建 `.venv` 并重新选择解释器。升级 Node.js 时同步更新 `.nvmrc` 和 `.vscode/launch.json` 的 `runtimeVersion`。 [VS Code Node.js 调试文档](https://code.visualstudio.com/docs/nodejs/nodejs-debugging#_multi-version-support)

## 本地 Codex 定制

根目录的公共 Codex 配置、导演 skill、角色和提示词可随仓库分发。个人覆盖文件与其他本地配置由 Git 忽略。写入 `~/.codex/config.toml` 的设置属于用户级，会跨项目生效。
