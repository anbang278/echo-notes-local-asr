#!/usr/bin/env bash
# One-time public repository bootstrap. No ASR software is installed.
# Bash 3.2+ compatible. Only explicit --publish permits external writes.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd -P)"
OWNER="anbang278"
REPO="$OWNER/echo-notes-local-asr"
DESCRIPTION="Mac-first local ASR companion for Echo Notes: guided model setup, offline transcription and local service management."
MANIFEST="$ROOT/scripts/public-files.txt"
MODE="${1:---dry-run}"
export GH_HOST="github.com"
# Do not inherit a caller's alternate Git worktree/index settings.
unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE GIT_COMMON_DIR

fail() { printf '错误：%s\n' "$*" >&2; exit 1; }
usage() {
  printf '%s\n' '用法：bash scripts/create-github-repo.sh [--dry-run|--publish|--help]'
  printf '%s\n' '默认仅列出公开文件。--publish 创建 anbang278/echo-notes-local-asr 公开仓库并推送文档。'
  printf '%s\n' '需预先安装 Git 和 GitHub CLI，并登录 anbang278；不会请求或保存访问令牌。'
}
[[ $# -le 1 ]] || { usage; exit 2; }
case "$MODE" in
  --help) usage; exit 0 ;;
  --dry-run|--publish) ;;
  *) usage; exit 2 ;;
esac
[[ -f "$MANIFEST" && ! -L "$MANIFEST" ]] || fail '缺少普通文件 scripts/public-files.txt。'

FILES=()
while IFS= read -r file || [[ -n "$file" ]]; do
  case "$file" in ''|\#*) continue ;; esac
  case "$file" in
    /*|../*|*/../*|*/..|.git|.git/*|*\\*) fail "不安全的发布路径：$file" ;;
  esac
  [[ "$file" != *$'\r'* ]] || fail '发布清单必须使用 LF 换行。'
  [[ -f "$ROOT/$file" ]] || fail "缺少发布文件：$file"
  current="$ROOT/$file"
  while [[ "$current" != "$ROOT" ]]; do
    [[ ! -L "$current" ]] || fail "发布路径不能包含符号链接：$file"
    current="$(dirname "$current")"
  done
  for previous in "${FILES[@]+${FILES[@]}}"; do
    [[ "$previous" != "$file" ]] || fail "发布清单包含重复路径：$file"
  done
  FILES+=("$file")
done < "$MANIFEST"
[[ ${#FILES[@]} -gt 0 ]] || fail '发布清单为空。'

printf '目标：%s\n可见性：PUBLIC\n默认分支：main\n发布文件：\n' "$REPO"
printf '  %s\n' "${FILES[@]}"
if [[ "$MODE" == '--dry-run' ]]; then
  printf '\n仅展示清单，没有访问 GitHub，没有创建 Git 仓库。\n'
  exit 0
fi

command -v git >/dev/null 2>&1 || fail '未安装 Git。请先准备开发者 Git 环境。'
command -v gh >/dev/null 2>&1 || fail '未安装 GitHub CLI（gh）。请按 https://cli.github.com/ 安装并登录后再运行。'
[[ ! -e "$ROOT/.git" && ! -L "$ROOT/.git" ]] || fail '当前目录已有 Git 元数据；为防止覆盖，停止初始化。'
if git -C "$ROOT" rev-parse --show-toplevel >/dev/null 2>&1; then
  fail '当前目录位于既有 Git 仓库中；请把初始化包解压到独立目录后执行。'
fi
python3 "$ROOT/scripts/check_public_files.py"

gh auth status --hostname github.com >/dev/null 2>&1 || fail 'GitHub CLI 尚未登录；请执行 gh auth login --hostname github.com。'
LOGIN="$(gh api --hostname github.com user --jq .login)"
[[ "$LOGIN" == "$OWNER" ]] || fail "当前 GitHub 账号为 ${LOGIN}，不是 ${OWNER}；未创建仓库。"
if gh repo view "$REPO" --json nameWithOwner >/dev/null 2>&1; then
  fail '同名远端仓库已经可见，停止创建；本脚本不会覆盖、追加或改变已有仓库可见性。'
fi
# A failed read can mean absence, network trouble, or inaccessible data.
# gh repo create is authoritative; any conflict/error aborts without overwrite.

git -C "$ROOT" init
# Works with older Git releases without relying on `git init -b`.
git -C "$ROOT" symbolic-ref HEAD refs/heads/main
git -C "$ROOT" add -- "${FILES[@]}"
git -C "$ROOT" -c user.name="$OWNER" \
  -c user.email="99390732+$OWNER@users.noreply.github.com" \
  commit -m 'chore: initialize Local ASR repository and Trellis development workflow'

if ! gh repo create "$REPO" --public --description "$DESCRIPTION" \
  --source "$ROOT" --remote origin --push; then
  printf '%s\n' '创建或推送未完成。保留本地提交，不自动删除任何远端仓库。' >&2
  printf '%s\n' '请检查是否已创建空仓库或已推送部分内容；核验后人工继续，勿盲目重复初始化。' >&2
  exit 1
fi

gh repo edit "$REPO" --default-branch main
VISIBILITY="$(gh repo view "$REPO" --json visibility --jq .visibility)"
BRANCH="$(gh repo view "$REPO" --json defaultBranchRef --jq .defaultBranchRef.name)"
LOCAL_SHA="$(git -C "$ROOT" rev-parse HEAD)"
REMOTE_SHA="$(gh api --hostname github.com "repos/$REPO/commits/main" --jq .sha)"
[[ "$VISIBILITY" == 'PUBLIC' ]] || fail '远端公开状态核验失败，请检查实际仓库；不自动更改已有内容。'
[[ "$BRANCH" == 'main' ]] || fail '远端默认分支核验失败。'
[[ "$REMOTE_SHA" == "$LOCAL_SHA" ]] || fail '远端 main 提交与本地不一致，不能报告发布完成。'

printf '\n已核验公开仓库：https://github.com/%s\n分支：%s\n提交：%s\n' "$REPO" "$BRANCH" "$REMOTE_SHA"
printf '%s\n' '请更新研发计划的建库状态并保留上述核验记录。ASR 应用尚未开发或部署。'
