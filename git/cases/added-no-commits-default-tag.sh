#!/bin/bash
set -ex

git init -b main

patch -p2 < "$PATCHDIR"/0100-code.diff
patch -E -p2 < "$PATCHDIR"/0200-packaged.diff
rmdir mypackage
patch -p2 < "$PATCHDIR"/0300-default-tag.diff
git add .
