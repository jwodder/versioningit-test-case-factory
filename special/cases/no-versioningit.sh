#!/bin/bash
set -ex

git init -b main

rsync -vaz "$TREEDIR"/unpackaged/ .
git add .
git commit -m "Code"

git tag v0.0.0

rsync -vaz --exclude=.git --delete "$TREEDIR"/no-versioningit/ .
git add -A
git commit -m "Packaging without versioningit"
