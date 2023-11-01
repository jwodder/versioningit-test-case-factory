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

patch -p2 < "$PATCHDIR"/0300-feature.diff
git add -A
git commit -m "Add a feature"

patch -p2 < "$PATCHDIR"/0400-onbuild.diff
git add -A
git commit -m "Use onbuild"

patch -p2 < "$PATCHDIR"/0500-onbuild-nonidem.diff
git add -A
git commit -m "Use onbuild non-idempotently"