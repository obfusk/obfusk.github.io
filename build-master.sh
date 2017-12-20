#!/bin/bash

set -ex

git checkout master

rsync_cmd=(
  rsync -av --delete __html__/ ./
    --exclude=.git --exclude='*~' --exclude=/__html__ --exclude=/old
    --exclude=/.gitignore --exclude=/.nojekyll --exclude=/CNAME
    --exclude=/deps
)

"${rsync_cmd[@]}" --dry-run
read -r -p 'continue [y/N]? '
[[ "$REPLY" = [Yy]* ]] || exit 1
"${rsync_cmd[@]}"

git add -A
git status

if [ -n "$( git status -s )" ]; then
  read -r -p 'continue [y/N]? '
  [[ "$REPLY" = [Yy]* ]] || exit 1
  git commit -m 'updated by build-master.sh'
fi

git checkout code
