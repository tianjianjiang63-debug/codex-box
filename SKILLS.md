# 本机技能与云端兼容性

此表对应 2026-10-18 本次聊天可见的技能。它不包含个人文件、模板、登录态、缓存或账号密钥。原始桌面插件的安装状态与云端能力不是同一个概念。

## 安装脚本实际提供什么

执行 `sh scripts/setup.sh` 后，从固定上游提交安装 **22 个公开技能**，加上仓库内 **3 个云端适配技能**，合计 **25 个技能入口**。最终以 `.work/skills-installed.json` 和 `.work/cloud-doctor.json` 为准，不能仅凭本表宣称已在云端装好。

| 本机技能 | 本仓库方案 | 能力边界 |
| --- | --- | --- |
| ppt-master | 完整官方 6.7.0，固定提交安装 | 运行完整性检查；本机模板另行提供；WPS/PowerPoint 专属操作不可移入云端 |
| pdf:pdf | 安装 OpenAI 公开版 pdf 技能 | 与桌面私有打包版本不同；文件读写、抽取与渲染可用 |
| documents:documents | cloud-documents | python-docx + 原生 OOXML + LibreOffice；不是专有文档会话运行时 |
| spreadsheets:Spreadsheets | cloud-spreadsheets | openpyxl/XlsxWriter + LibreOffice；不是 artifact-tool |
| presentations:Presentations | cloud-presentations，或按指定使用 ppt-master | 文件处理；不是 artifact-tool/原生云端幻灯片服务 |
| openai-docs | OpenAI 公开版固定提交安装 | 外部文档检索还需宿主搜索工具或允许的网络 |
| skill-creator | OpenAI 公开版固定提交安装 | 可创建仓库内技能；不赋予额外账号权限 |
| skill-installer | OpenAI 公开版固定提交安装 | 安装源仍需网络；不会覆盖现有同名技能 |
| imagegen | OpenAI 公开版固定提交安装 | 需要宿主 imagegen 工具，或按技能要求配置 API key；没有迁移桌面额度或凭据 |
| agent-reach | 官方 1.5.0 技能及同提交 CLI | 可运行 `.venv/bin/agent-reach doctor --json`；云端网络域名、第三方 CLI 与登录态仍按渠道配置 |
| cnki-search | 条件依赖，未宣称已装好服务 | 云端须另接可访问的 cnki-mcp 与机构认证；本机 Profile 不复制 |
| explore-cnki-view | 继续在本机使用 | 当前官方云端环境不支持浏览器/computer use；不宣称可在云端复现页面下载 |
| computer-use:computer-use | 继续在本机使用 | Windows 桌面、用户浏览器及登录态不可由本仓库复制 |
| spreadsheets:excel-live-control | 连接能力，不打包 | 需受支持的 Excel 会话和宿主工具 |
| visualize:visualize | 宿主能力，不打包 | 科学静态绘图可用 matplotlib；交互渲染不能靠复制技能获得 |
| template-creator:template-creator | 条件依赖，未克隆桌面插件 | 可用 skill-creator 创建文件模板技能；原生模板服务和用户模板需单独提供 |
| write-like-me:write-like-me | 条件依赖，未克隆桌面插件 | 写作样本/风格档案不会自动同步，可在具体任务中提供 |
| plugin-management:plugin-management | 宿主连接与插件界面 | 不把本机插件配置或账号凭据写入 Git |
| sites:sites | 宿主 Sites 连接 | 发布、域名和项目身份由服务连接管理 |

## Superpowers

以下 **15 个技能**均从官方 6.4.2 安装，保留原始指令和许可。它们给出工作方法，不会提供云端原本不存在的子代理、代码审查服务或 Windows 工具。用户的明确授权和宿主规则优先。

- brainstorming
- diagnosing-superpowers
- dispatching-parallel-agents
- executing-plans
- finishing-a-development-branch
- receiving-code-review
- requesting-code-review
- subagent-driven-development
- systematic-debugging
- test-driven-development
- using-git-worktrees
- using-superpowers
- verification-before-completion
- writing-plans
- writing-skills

## 依赖外部插件工具的技能

这些插件指令未复制到仓库。先在具体云端任务中确认对应工具已出现；没有工具时只写“需连接”，不能报告已安装对应服务。

| 插件 | 本次可见技能 |
| --- | --- |
| Codex Security | assess-patch-risk、attack-path-analysis、deep-security-scan、define-security-policy、finding-discovery、fix-finding、propose-security-hardening、security-diff-scan、security-scan、threat-model、track-findings、triage-finding、validation、verify-fix、vulnerability-writeup |
| Figma | figma-code-connect、figma-code-workflows、figma-create-new-file、figma-design-to-code、figma-generate-design、figma-generate-diagram、figma-generate-library、figma-generative-plugins、figma-implement-motion、figma-shaders、figma-spec、figma-swiftui、figma-use、figma-use-figjam、figma-use-motion、figma-use-slides |
| Google Drive | google-docs、google-drive、google-drive-comments、google-sheets、google-slides |
| ChatGPT Pets | create-pet、pets、update-pet |

Gmail、Google Calendar、Google Contacts、GitHub、Atlassian 和 Linear 在本次会话中以连接工具提供；它们也不是 pip 包或可由本安装脚本创建的授权。Gmail 已在本聊天连接不等于新云端任务已验证 Gmail 可用。

## 版本与来源

- PPT Master：https://github.com/hugohe3/ppt-master ，6.7.0，MIT。
- Superpowers：https://github.com/obra/superpowers ，6.4.2，MIT。
- OpenAI 公开技能：https://github.com/openai/skills ，固定快照，保留每个技能自带的许可与完整资源。
- Agent Reach：https://github.com/Panniantong/Agent-Reach ，1.5.0，MIT；技能文件与 CLI 均锁定到同一提交。
- 本仓库三个 cloud-* 技能为云端适配指令，明确标注与桌面插件的区别。
- 上游提交锁定见 skills.lock.json；安装器来自同一锁定的 OpenAI skill-installer。安装第三方技能时不会去除归属、许可或完整性检查。

官方依据：https://learn.chatgpt.com/docs/environments/cloud-environments 。其中说明仓库内技能可供云端任务使用，本机个人技能不会自动同步；当前云端环境不支持 computer/browser use。
