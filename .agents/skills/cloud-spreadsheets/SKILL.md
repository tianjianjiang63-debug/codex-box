---
name: cloud-spreadsheets
description: 在云端处理 XLSX、CSV 和 TSV 文件的公式、数据、格式和图表；不用于控制桌面 Excel 或代替 Google Sheets 账号连接。
---

# 云端表格文件

这是公开 Python 文件库的适配工作流，不等同于桌面 artifact-tool 或 Excel 实时控制。

使用 `.venv/bin/python`、openpyxl 和 XlsxWriter。先检查工作表、数据范围、公式、合并区域及样式。已有表格只改授权范围；保留公式，避免读 data_only=True 后保存导致公式丢失。宏、外链或复杂图表要先确认所用库的保留能力。

openpyxl 不计算公式。需要计算结果时，用 `.venv/bin/python scripts/render_office.py 输入.xlsx work/新的预览目录 --png` 经 LibreOffice 重算并检查显示；若需返回带缓存的 XLSX，应在新目录做 LibreOffice XLSX 转存后回读 data_only=True，核对代表性公式的输入与结果。LibreOffice 不支持的 Excel 函数应说明，不编造缓存值。

检查表头、日期和数值单位、筛选、冻结、列宽、公式引用和打印区域。公式检查与预览都通过后交付 outputs/ 的可编辑文件。仅需 CSV 时保留原编码、字段语义与必要的转义。原生 Google Sheets 或实时 Excel 操作需要实际连接工具。
