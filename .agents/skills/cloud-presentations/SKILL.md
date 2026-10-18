---
name: cloud-presentations
description: 在没有桌面 PowerPoint/WPS 或专有演示运行时的云端环境中处理可编辑 PPTX 文件；指定 PPT Master 的任务使用已安装的 ppt-master 技能。
---

# 云端 PPT 文件

这是公开文件库的云端适配工作流，不是桌面 presentations 插件的专有 artifact-tool 运行时。

用户指定 PPT Master 时读取 `.agents/skills/ppt-master/SKILL.md` 并按原始入口执行；完整性检查失败则停止该技能，不修改检查器来继续。

其他 PPTX 文件任务可用 `.venv/bin/python`、python-pptx 与 OOXML。先检查源文件尺寸、母版、布局、字体、备注、图表、公式、动画和媒体；编辑已有课件时保持源文件，按用户范围修改并交付新文件。不要用全页图片代替用户要求的可编辑对象。

复杂公式保留原生结构，图表与表格保留可编辑数据。python-pptx 不能安全往返某种对象时，保留其原 XML，或说明能力缺口；不能声称普通往返保存会保留一切。

运行 `.venv/bin/python scripts/render_office.py 输入.pptx work/新的预览目录 --png`，逐页检查文字遮挡、字号、公式、图像、表格、备注和页数；同时用 ZIP/XML 检查原生对象与用户要求的保留项。LibreOffice 静态渲染不能验证 PowerPoint 动画播放、切换或录音效果。

成品放 outputs/；模板、媒体和源材料必须在云端任务可访问。涉及 Figma Slides 或 Google Slides 时，仅调用当前实际连接的服务。
