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

git tag rel_0_1_0

patch -p2 < "$PATCHDIR"/0300-custom-method.diff
git add -A
git commit -m "Use a custom method inside package for tag2version"

patch -p2 < "$PATCHDIR"/0400-custom-method-pkg.diff
git add -A
git commit -m "Import custom method from package"
