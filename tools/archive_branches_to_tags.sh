#!/usr/bin/env bash
# Archive every remote branch except the kept ones as a lightweight tag archive/<branch>, verify, then delete the branch.
# Commits stay reachable through the tags (nothing is lost); open PRs from deleted branches are closed by GitHub.
#
#   tools/archive_branches_to_tags.sh            # dry run: prints the plan
#   tools/archive_branches_to_tags.sh --apply    # creates + verifies the tags, then deletes the branches
#
# Run it from a normal clone on your own computer (needs push rights; tag pushes are blocked in the Claude sandbox).
set -euo pipefail
KEEP_REGEX='^(main)$'
APPLY=${1:-}
REMOTE=origin
git fetch --quiet "$REMOTE" --prune
mapfile -t LINES < <(git ls-remote --heads "$REMOTE" | sed 's#refs/heads/##')
plan=()
for l in "${LINES[@]}"; do
  sha=${l%%$'\t'*}; br=${l#*$'\t'}
  [[ $br =~ $KEEP_REGEX ]] && continue
  tag="archive/${br#archive/}"
  plan+=("$sha $br $tag")
done
printf '%s branches to archive (keeping: %s)\n' "${#plan[@]}" "$KEEP_REGEX"
printf '  %s\n' "${plan[@]}" | head -n 400
[[ $APPLY == --apply ]] || { echo "dry run — re-run with --apply"; exit 0; }
# 1) tags (in batches of 40 refspecs)
specs=()
for p in "${plan[@]}"; do read -r sha br tag <<<"$p"; specs+=("$sha:refs/tags/$tag"); done  # tips are local after the fetch above
for ((i=0; i<${#specs[@]}; i+=40)); do git push "$REMOTE" "${specs[@]:i:40}"; done
# 2) verify every tag points at the branch tip
remote_tags=$(git ls-remote --tags "$REMOTE")
for p in "${plan[@]}"; do read -r sha br tag <<<"$p"; grep -q "^$sha	refs/tags/$tag$" <<<"$remote_tags" || { echo "tag missing for $br — aborting before any deletion"; exit 1; }; done
echo "all ${#plan[@]} tags verified"
# 3) delete branches
dels=(); for p in "${plan[@]}"; do read -r sha br tag <<<"$p"; dels+=(":refs/heads/$br"); done
for ((i=0; i<${#dels[@]}; i+=40)); do git push "$REMOTE" "${dels[@]:i:40}"; done
git ls-remote --heads "$REMOTE"
