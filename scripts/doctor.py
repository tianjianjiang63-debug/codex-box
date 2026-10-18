"""Report file-tool readiness; external account connections remain unverified."""
from __future__ import annotations

import argparse
import importlib.util
import json
import platform
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
MODULES = ["docx", "openpyxl", "pptx", "xlsxwriter", "pypdf", "pdfplumber", "reportlab", "fitz", "PIL", "matplotlib", "yaml", "lxml", "requests", "bs4", "pathops", "uharfbuzz"]


def diagnose() -> dict:
    lock = json.loads((ROOT / "skills.lock.json").read_text(encoding="utf-8"))
    state_path = ROOT / ".work" / "skills-installed.json"
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
    skills = {}
    for source in lock["sources"]:
        for path in source["paths"]:
            name = Path(path).name
            skills[name] = {
                "present": (ROOT / ".agents" / "skills" / name / "SKILL.md").is_file(),
                "source_matches": state.get(name) == {"repo": source["repo"], "ref": source["ref"], "path": path},
            }
    for name in ["cloud-documents", "cloud-spreadsheets", "cloud-presentations"]:
        skills[name] = {"present": (ROOT / ".agents" / "skills" / name / "SKILL.md").is_file(), "source_matches": True}
    binaries = {"libreoffice": shutil.which("libreoffice") or shutil.which("soffice"), "pdftoppm": shutil.which("pdftoppm"), "git": shutil.which("git")}
    fonts = None
    if shutil.which("fc-match"):
        fonts = subprocess.check_output(["fc-match", "Noto Sans CJK SC"], text=True).strip()
    report = {
        "platform": platform.system(), "python": sys.version.split()[0],
        "python_version_ok": sys.version_info >= (3, 11),
        "modules": {name: importlib.util.find_spec(name) is not None for name in MODULES},
        "binaries": binaries, "cjk_font_match": fonts, "skills": skills,
        "external_connections": "not tested; confirm the task's actual connector/MCP tools",
        "cloud_environment_published": "not verified by this local report",
    }
    report["ready"] = report["python_version_ok"] and all(report["modules"].values()) and all(binaries.values()) and all(s["present"] and s["source_matches"] for s in skills.values())
    output = ROOT / ".work" / "cloud-doctor.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    report = diagnose()
    print(json.dumps(report, indent=2, ensure_ascii=False))
    raise SystemExit(1 if args.strict and not report["ready"] else 0)
