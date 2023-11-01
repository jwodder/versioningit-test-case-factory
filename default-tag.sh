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

patch -p2 < "$PATCHDIR"/0300-default-tag.diff
hg addremove
hg commit -m "Set default-tag"
