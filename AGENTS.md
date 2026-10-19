# Codex Cloud 工作约定

这是一个技能工作区。先读 README.md 和 SKILLS.md，区分已安装的文件技能与尚需连接的外部服务。

## 环境

- 安装入口：`sh scripts/setup.sh`。命令失败时保留错误，不把未完成安装报告为成功。
- Python 使用本仓库 `.venv/bin/python`；不要覆盖系统 Python 或修改用户级 Codex 配置。
- 若 `.work/cloud-doctor.json` 不存在，运行 `.venv/bin/python scripts/doctor.py`；缺少 `.venv` 时先完成安装。
- 第三方技能位于 `.agents/skills/`，使用前阅读相应 SKILL.md。下载和安装状态见 `.work/skills-installed.json`。
- Agent Reach 的命令行程序位于 `.venv/bin/agent-reach`；使用它前运行 `.venv/bin/agent-reach doctor --json`，渠道状态记录在 `.work/agent-reach-doctor.json`。新任务中的 shell 不一定继承安装脚本的 PATH，调用时使用完整路径或先激活 `.venv`。
- Agent Reach 需要外网和各平台的独立登录条件；技能或 CLI 已安装不代表 Twitter、小红书等登录渠道可用。不要把 Cookie 或访问令牌写入仓库。
- 新技能首次安装后可能需要下一轮任务才能被宿主发现。文件存在不等于宿主工具、账户连接或 API 凭据可用。
- 按宿主实际工具列表验证 Gmail、Drive、Figma、CNKI、图像生成、子代理、安全扫描等能力；不猜工具名，不把账号权限写进仓库。

## 文件交付

- 输入材料须来自本任务已获准访问的文件；本机文件、模板、历史记忆及浏览器登录态不会自动同步。
- 临时文件放 work/，最终成品放 outputs/，非用户要求不要把个人材料提交到 Git。
- Word/表格/PPT 使用对应 cloud-* 适配技能；指定 PPT Master 时保留其完整官方技能和完整性检查，不修改其门禁文件。
- Office 文件保持可编辑性；复杂公式保留原生结构，已有模板、动画、媒体和备注按用户范围处理。
- 交付前做结构回读和实际渲染检查。LibreOffice 与 WPS/PowerPoint 的字体、动画或排版可能不同，不能把云端渲染说成已在 WPS/PowerPoint 验证。
- 不在仓库保存密钥、.env、浏览器 Profile、cookie、MCP 账号配置或宿主插件缓存。
