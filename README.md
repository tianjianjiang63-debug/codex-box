# codex-box

Codex 云端技能与文件处理工作区。配置日期：2026-10-18。

## 启用

在 Codex Cloud 创建环境并选择 `tianjianjiang63-debug/codex-box`。将下面命令填入 Install script（旧界面为 Setup script），或发给环境配置助手执行：

```sh
sh scripts/setup.sh
```

安装完成后，检查 `.work/cloud-doctor.json`，再发布环境。新任务先读取 `AGENTS.md`；安装完成前不要声称所有技能可用。

安装脚本面向 Ubuntu/Debian 云端环境：创建仓库内 `.venv`，安装 Word/PDF/Excel/PPT 处理依赖、LibreOffice、Poppler、中文字体、Agent Reach CLI，并从固定提交安装公开技能。无需 GitHub PAT，也无需提供 OpenAI API key 来完成基础安装。

网络至少放行包管理器预设，并补充 `raw.githubusercontent.com`；首次安装需要 `github.com`、`codeload.github.com`、PyPI 和 Ubuntu 软件源。若要在云端任务中用 Agent Reach 读取网页、V2EX、B站公开内容，可按需放行 `r.jina.ai`、`www.v2ex.com`、`api.bilibili.com`；其他平台按实际任务增加域名和登录条件。不要在环境内使用 Windows 本机代理地址。

## 技能范围

- PPT Master **6.7.0**、Superpowers **6.4.2**：固定到与本机版本一致的上游提交，保留原始文件、归属与许可。
- OpenAI 公开版 PDF、OpenAI Docs、skill-creator、skill-installer、imagegen：固定提交安装。
- Agent Reach **1.5.0**：官方 SKILL.md 与 CLI 都锁定到同一上游提交。CLI 位于 `.venv/bin/agent-reach`；登录态和第三方渠道单独配置。
- `cloud-documents`、`cloud-spreadsheets`、`cloud-presentations`：本仓库的云端适配工作流，使用公开文件库，不冒充桌面端专有运行时。
- 完整技能对照见 [SKILLS.md](SKILLS.md)。Gmail、Google Drive、Figma 等需在云端任务中确认连接；仅安装 SKILL.md 不会安装相应服务端工具。

图像生成依赖宿主图像工具，或按公开 imagegen 技能配置 API 凭据；基础安装不测试付费调用。知网需要能访问的 MCP 服务及机构认证。浏览器/computer use、Windows COM、WPS/PowerPoint、桌面宠物等不能由本安装脚本迁入云端。

## 使用与检查

```sh
.venv/bin/python scripts/doctor.py --strict
.venv/bin/agent-reach doctor --json
.venv/bin/python scripts/smoke_artifacts.py --render
```

自检会实际创建并回读 DOCX、XLSX、PPTX、PDF；`--render` 还通过 LibreOffice 转换三个 Office 文件并检查 PDF。Agent Reach 渠道状态另见 `.work/agent-reach-doctor.json`；其中未配置的渠道不影响文件处理自检通过。自检不是人工视觉验收，也不证明账号连接已可用。初次安装后开启新一轮任务让宿主重新发现技能。

工作文件放 `work/`，成品放 `outputs/`。下载的技能、虚拟环境、测试输出均不提交。仓库当前为公开仓库；个人文档及模板不要随意提交，改为私有或使用任务支持的私密文件入口。

## 更新

脚本可重复运行。同一版本不会重复下载技能；已经存在但未登记来源的同名技能不会被覆盖。需要更新时先修改 `skills.lock.json` 中的固定提交，经检查后重新安装；版本冲突会停止并给出路径，不会自动删除你的改动。

云端配置保存后还须 Publish/Republish 才能用于新任务。仓库提交不等于已经创建、发布或验证了云端环境。
