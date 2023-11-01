#!/bin/bash
set -ex

git init -b main

rsync -vaz "$TREEDIR"/no-versioningit/ .
git add .
git commit -m "Packaging without versioningit"

git tag v0.1.0
