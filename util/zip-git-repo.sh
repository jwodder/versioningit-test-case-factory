#!/bin/bash
# The zipfile path must be absolute.
repo="${1:?Usage: $0 git-repo zipfile}"
zipfile="${2:?Usage: $0 git-repo zipfile}"

cd "$repo"
git gc --aggressive --prune=now
zip --exclude "*.sample" -r "$zipfile" .
