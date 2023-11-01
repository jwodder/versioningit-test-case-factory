#!/bin/bash
set -ex

git init -b main

rsync -vaz "$TREEDIR"/no-pyproject/ .
git add .
git commit -m "Packaging with setup.py"

git tag v0.1.0
