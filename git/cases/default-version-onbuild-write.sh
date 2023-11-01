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

git tag 0.1.0

patch -p2 < "$PATCHDIR"/0300-default-version2.diff
git add -A
git commit -m "Use default-version"

patch -p2 < "$PATCHDIR"/0400-write-onbuild.diff
git add -A
git commit -m "Use write & onbuild"
