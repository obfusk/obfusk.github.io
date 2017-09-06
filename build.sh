#!/bin/bash

set -e

git checkout master
cp -av __html__/* ./
git add -A
git status

read -r -p 'continue [y/N]? '
[[ "$REPLY" = [Yy]* ]] || exit 1

git commit -m ...
git checkout code
