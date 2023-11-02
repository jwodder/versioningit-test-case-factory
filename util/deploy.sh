#!/bin/bash
set -eux
repo="${1:?Usage: $0 versioningit-repo}"
repo="$(realpath "$repo")"

cd "$(dirname "$0")"/../target

rm -f "$repo"/test/data/*.tar.gz
cp -f *.tar.gz "$repo"/test/data

rsync -vaz repos/ "$repo"/test/data/repos
