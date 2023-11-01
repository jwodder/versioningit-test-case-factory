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

git tag v0.1.0

patch -p2 < "$PATCHDIR"/0300-default-version.diff
git add -A
git commit -m "Use default-version"

patch -p2 < "$PATCHDIR"/0400-default-version-bad.diff
git add -A
git commit -m "Use a non-PEP 440 default-version"
