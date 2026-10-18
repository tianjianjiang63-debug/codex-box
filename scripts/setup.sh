#!/bin/sh
set -eu
TASK_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$TASK_ROOT"

if [ "$(uname -s)" != Linux ]; then
  echo 'This setup targets Linux Codex Cloud. Local Windows settings are unchanged.' >&2
  exit 2
fi

if ! command -v apt-get >/dev/null 2>&1; then
  echo 'Ubuntu/Debian with apt-get is required for the Office rendering stack.' >&2
  exit 2
fi

if [ "$(id -u)" -eq 0 ]; then
  apt-get update
  DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3 python3-venv git ca-certificates libreoffice-writer libreoffice-calc \
    libreoffice-impress poppler-utils fonts-noto-cjk fonts-liberation fontconfig
elif command -v sudo >/dev/null 2>&1 && sudo -n true 2>/dev/null; then
  sudo -n apt-get update
  sudo -n env DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    python3 python3-venv git ca-certificates libreoffice-writer libreoffice-calc \
    libreoffice-impress poppler-utils fonts-noto-cjk fonts-liberation fontconfig
else
  echo 'No noninteractive apt permission. Checking preinstalled tools instead.'
  command -v libreoffice >/dev/null 2>&1 || command -v soffice >/dev/null 2>&1 || {
    echo 'Missing LibreOffice. Have the cloud environment setup install it, then rerun.' >&2
    exit 2
  }
  command -v pdftoppm >/dev/null 2>&1 || { echo 'Missing poppler-utils.' >&2; exit 2; }
fi

python3 -m venv .venv
TASK_PYTHON="$TASK_ROOT/.venv/bin/python"
"$TASK_PYTHON" -m pip install --disable-pip-version-check -r requirements.txt
"$TASK_PYTHON" scripts/install_skills.py
"$TASK_PYTHON" scripts/doctor.py --strict
"$TASK_PYTHON" scripts/smoke_artifacts.py --render
echo 'Setup passed. Review .work/cloud-doctor.json, then publish the cloud environment.'
