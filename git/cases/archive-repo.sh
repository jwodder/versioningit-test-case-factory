#!/bin/bash
set -ex

git init -b main

patch -p2 < "$PATCHDIR"/0100-code.diff
git add .
git commit -m "Some code"

patch -E -p2 < "$PATCHDIR"/0200-packaged.diff
rmdir mypackage
git add -A
git commit -m "Packaging"

git tag -m 'Version 0.1.0' v0.1.0

patch -p2 < "$PATCHDIR"/0300-archive.diff
git add -A
git commit -m "Switch to git-archive"
