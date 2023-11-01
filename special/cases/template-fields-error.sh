#!/bin/bash
set -ex

git init -b main

rsync -vaz "$TREEDIR"/base/ .
git add .
git commit -m "Packaging"

git tag v0.1.0

rsync -vaz --exclude=.git --delete "$TREEDIR"/template-fields-error/ .
git add -A
git commit -m "Set us up for failure"
