#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
venv_dir="${repo_root}/.git/.skill-validator-venv"
python_bin="${PYTHON:-python3}"

if [[ ! -x "${venv_dir}/bin/python" ]]; then
  "${python_bin}" -m venv "${venv_dir}"
fi

"${venv_dir}/bin/python" - <<'PY'
from importlib.util import find_spec
import subprocess
import sys

if find_spec("yaml") is None:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "--quiet", "pyyaml"])
PY

exec "${venv_dir}/bin/python" "${repo_root}/scripts/validate_skills.py" "$@"
