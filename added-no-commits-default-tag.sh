#!/bin/bash
set -ex

PATCHDIR="$(dirname "$0")"/patches

hg init

patch -p2 < "$PATCHDIR"/0100-code.diff
patch -p2 < "$PATCHDIR"/0200-packaged.diff
rm mypackage/code.py
rmdir mypackage
patch -p2 < "$PATCHDIR"/0300-default-tag.diff
hg add
