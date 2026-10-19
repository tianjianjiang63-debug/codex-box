"""Install immutable public skills using OpenAI's upstream skill installer."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def download(url: str, destination: Path) -> None:
    request = urllib.request.Request(url, headers={"User-Agent": "codex-box-bootstrap"})
    with urllib.request.urlopen(request, timeout=120) as response:
        payload = response.read()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_bytes(payload)


def install(only_repo: str | None = None) -> dict:
    lock = json.loads((ROOT / "skills.lock.json").read_text(encoding="utf-8"))
    helper_ref = lock["helper_ref"]
    if not re.fullmatch(r"[0-9a-f]{40}", helper_ref):
        raise ValueError("Installer must be pinned to an immutable commit.")
    work = ROOT / ".work"
    state_path = work / "skills-installed.json"
    state = json.loads(state_path.read_text(encoding="utf-8")) if state_path.exists() else {}
    helper_dir = work / "installer" / helper_ref
    for name in ("github_utils.py", "install-skill-from-github.py"):
        destination = helper_dir / name
        if not destination.exists():
            download(f"https://raw.githubusercontent.com/openai/skills/{helper_ref}/skills/.system/skill-installer/scripts/{name}", destination)
    destination_root = ROOT / ".agents" / "skills"
    destination_root.mkdir(parents=True, exist_ok=True)
    selected = [s for s in lock["sources"] if only_repo is None or s["repo"] == only_repo]
    if not selected:
        raise ValueError("No source matches --only-repo.")
    for source in selected:
        if not re.fullmatch(r"[0-9a-f]{40}", source["ref"]):
            raise ValueError("Every source must be pinned to an immutable commit.")
        if source.get("license_path"):
            download(f"https://raw.githubusercontent.com/{source['repo']}/{source['ref']}/{source['license_path']}", ROOT / ".agents" / "third-party" / (source["repo"].replace("/", "-") + "-LICENSE"))
        pending = []
        for skill_path in source["paths"]:
            name = source.get("names", {}).get(skill_path, Path(skill_path).name)
            identity = {"repo": source["repo"], "ref": source["ref"], "path": skill_path}
            target = destination_root / name
            if target.exists():
                if state.get(name) != identity or not (target / "SKILL.md").is_file():
                    raise RuntimeError(f"Unmanaged or incompatible skill at {target}; preserve it and resolve the conflict explicitly.")
                print(f"Already installed: {name}", flush=True)
                continue
            pending.append((name, skill_path, identity))
        if pending:
            print(f"Installing {len(pending)} skills from {source['repo']} at {source['ref']}", flush=True)
            command = [sys.executable, str(helper_dir / "install-skill-from-github.py"), "--repo", source["repo"], "--ref", source["ref"], "--path", *[p for _, p, _ in pending], "--dest", str(destination_root), "--method", "download"]
            if len(pending) == 1 and pending[0][0] != Path(pending[0][1]).name:
                command.extend(["--name", pending[0][0]])
            subprocess.run(command, check=True, timeout=1200)
            for name, _, identity in pending:
                state[name] = identity
            work.mkdir(parents=True, exist_ok=True)
            state_path.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        if source["repo"] == "hugohe3/ppt-master":
            subprocess.run([sys.executable, str(destination_root / "ppt-master" / "scripts" / "attribution_guard.py")], check=True, timeout=60)
    return state


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--only-repo", help="Install one locked source for diagnostics.")
    args = parser.parse_args()
    install(args.only_repo)
