#!/usr/bin/env python3
import argparse
from datetime import datetime, timezone
from pathlib import Path
import shutil
import subprocess


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--outfile", type=argparse.FileType("w"), default="-")
    parser.add_argument("repo", type=Path)
    parser.add_argument("infile", type=argparse.FileType("r"))
    args = parser.parse_args()
    # Check whether the repository has any commits in it, because if it
    # doesn't, the next command won't work.
    r = subprocess.run(
        ["git", "rev-list", "-n1", "--all"],
        cwd=args.repo,
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    )
    if r.stdout.strip():
        r = subprocess.run(
            ["git", "--no-pager", "show", "-s", "--format=%h%n%H%n%at%n%ct"],
            cwd=args.repo,
            stdout=subprocess.PIPE,
            text=True,
            check=True,
        )
        rev, revision, author_ts, committer_ts = r.stdout.splitlines()
        author_date = datetime.fromtimestamp(int(author_ts), tz=timezone.utc)
        committer_date = datetime.fromtimestamp(int(committer_ts), tz=timezone.utc)
        with args.infile, args.outfile:
            for line in args.infile:
                line = (
                    line.replace("{hash}", rev)
                    .replace("{revision}", revision)
                    .replace("{author_date}", str(author_date))
                    .replace("{committer_date}", str(committer_date))
                )
                print(line, file=args.outfile, end="")
    else:
        shutil.copyfileobj(args.infile, args.outfile)


if __name__ == "__main__":
    main()
