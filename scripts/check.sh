#!/usr/bin/env bash
# Repository/bootstrap checks only; no ASR installation or remote operation.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
export PYTHONDONTWRITEBYTECODE=1
python3 scripts/check_public_files.py
python3 scripts/validate-docs.py
bash -n scripts/create-github-repo.sh
python3 -m unittest discover -s tests -v
while IFS= read -r task_file; do
  python3 .trellis/scripts/task.py validate "$(dirname "$task_file")"
done < <(find .trellis/tasks -type f -name task.json | sort)
python3 .trellis/scripts/get_context.py --mode packages
python3 .trellis/scripts/get_context.py --mode phase --step 1.1 --platform codex >/dev/null
printf '%s\n' 'PASS: repository governance checks. ASR, clean Mac and signing remain unverified.'
