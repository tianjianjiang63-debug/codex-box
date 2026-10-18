---
name: cloud-documents
description: 在没有桌面 Office 或专有文档运行时的云端环境中创建、编辑和检查 DOCX 文件；不用于控制本机 Word 或直接操作 Google Docs。
---

# 云端 Word 文件

本技能是云端文件工作流，不是桌面 documents 插件的原样副本。

使用仓库 `.venv/bin/python` 和 python-docx。已有文件先读取正文、段落样式、表格、页眉页脚、节设置及 ZIP 内嵌对象；仅修改用户要求的部分。python-docx 不支持的修订、评论、公式和媒体要保留原有 OOXML，复杂改动先确认所用方法能保存这些结构。

用 Word 段落样式控制标题和正文，复杂数学使用原生 OMML；不要用普通文本伪装可编辑分式或把公式全部转成截图。字体按模板及用户要求，检查云端是否实际安装对应字体；替代字体的渲染不能冒充原字体。

运行 `.venv/bin/python scripts/render_office.py 输入.docx work/新的预览目录 --png`，逐页检查 PNG，并回读关键文字、公式、表格及页数。扫描文档不把空的文本抽取当成空白页面。对用户成品始终做视觉检查；自动自检不替代视觉验收。

最终文件放 outputs/，附文件链接。说明影响使用的渲染或兼容性问题，不声称已在本机 Word/WPS 打开。Google Docs 原生文件使用当前任务实际提供的 Drive/Docs 连接工具。
