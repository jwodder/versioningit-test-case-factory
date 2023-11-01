#!/bin/bash
set -ex

hg init

patch -p2 < "$PATCHDIR"/0100-code.diff
hg add
hg commit -m "Some code"

patch -p2 < "$PATCHDIR"/0200-packaged.diff
rm mypackage/code.py
rmdir mypackage
hg addremove
hg commit -m "Packaging"

hg tag v0.1.0

patch -p2 < "$PATCHDIR"/0300-feature.diff
hg addremove
hg commit -m "Add a feature"

patch -p2 < "$PATCHDIR"/0300-pattern.diff
hg addremove
hg commit -m "Set vcs.pattern"

hg tag 0.2.0
