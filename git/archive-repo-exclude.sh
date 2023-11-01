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

git tag -m 'Version 0.1.0' 0.1.0

patch -p2 < "$PATCHDIR"/0300-archive-exclude.diff
git add -A
git commit -m "Switch to git-archive"

patch -p2 < "$PATCHDIR"/0300-feature.diff
git add -A
git commit -m "Add a feature"

git tag -m 'Version 0.2.0' v0.2.0
