from __future__ import annotations
from collections.abc import Sequence
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from importlib.resources import files
import json
from pathlib import Path
import re
import shutil
from .util import readcmd, runcmd, zipdir

BUILD_DATE = datetime(2038, 1, 19, 3, 14, 7, tzinfo=timezone.utc)


@dataclass
class Git:
    path: Path
    zipfile: Path

    def __post_init__(self) -> None:
        runcmd("git", "init", "-b", "main", "--", self.path)
        with (files("factory") / "data" / "gitignore").open(encoding="utf-8") as src:
            with (self.path / ".gitignore").open("w", encoding="utf-8") as dest:
                shutil.copyfileobj(src, dest)

    def rungit(self, *args: str) -> None:
        runcmd("git", *args, cwd=self.path)

    def commit(self, message: str) -> None:
        self.rungit("add", "-A")
        self.rungit("commit", "-m", message)

    def tag(self, name: str, message: str | None = None) -> None:
        cmd = ["tag"]
        if message is not None:
            cmd.extend(["-m", message])
        cmd.append(name)
        self.rungit(*cmd)

    def zip(self) -> None:
        zip_git(self.path, self.zipfile)

    def get_info(
        self, tags: bool = True, match: Sequence[str] = (), exclude: Sequence[str] = ()
    ) -> GitInfo:
        cmd = ["git", "describe", "--long", "--always"]
        if tags:
            cmd.append("--tags")
        for pat in match:
            cmd.append(f"--match={pat}")
        for pat in exclude:
            cmd.append(f"--exclude={pat}")
        describe = readcmd(*cmd, cwd=self.path)
        m = re.fullmatch(
            r"(?P<tag>.+)-(?P<distance>[0-9]+)-g(?P<rev>[0-9a-f]+)?", describe
        )
        if not m:
            raise ValueError(
                f"Could not parse `git describe` output for {self.path}: {describe!r}"
            )
        tag = m["tag"]
        assert isinstance(tag, str)
        distance = int(m["distance"])
        rev = m["rev"]
        assert isinstance(rev, str)
        revision, author_ts, committer_ts = readcmd(
            "git",
            "--no-pager",
            "show",
            "-s",
            "--format=%H%n%at%n%ct",
            cwd=self.path,
        ).splitlines()
        author_date = datetime.fromtimestamp(int(author_ts), tz=timezone.utc)
        committer_date = datetime.fromtimestamp(int(committer_ts), tz=timezone.utc)
        return GitInfo(
            author_date=author_date,
            committer_date=committer_date,
            distance=distance,
            rev=rev,
            revision=revision,
        )


@dataclass
class GitInfo:
    author_date: datetime
    build_date: datetime = field(init=False, default=BUILD_DATE)
    committer_date: datetime
    distance: int
    rev: str
    revision: str
    vcs: str = field(init=False, default="g")
    vcs_name: str = field(init=False, default="git")

    def save(self, path: Path) -> None:
        with path.open("w", encoding="utf-8") as fp:
            json.dump(asdict(self), fp, default=str)


@dataclass
class Mercurial:
    path: Path
    zipfile: Path

    def __post_init__(self) -> None:
        runcmd("hg", "init", "--", self.path)
        with (files("factory") / "data" / "hgignore").open(encoding="utf-8") as src:
            with (self.path / ".hgignore").open("w", encoding="utf-8") as dest:
                shutil.copyfileobj(src, dest)

    def runhg(self, *args: str) -> None:
        runcmd("hg", *args, cwd=self.path)

    def commit(self, message: str) -> None:
        self.runhg("addremove")
        self.runhg("commit", "-m", message)

    def tag(self, name: str) -> None:
        self.runhg("tag", name)

    def zip(self) -> None:
        zipdir(self.path, self.zipfile)

    def get_info(self, pattern: str | None = None) -> HGInfo:
        if pattern is None:
            template = "{latesttag() % '{tag}:{changes}:{node}\n'}"
        else:
            template = "{latesttag(" + repr(pattern) + ") % '{tag}:{changes}:{node}\n'}"
        _tag, sdistance, revision = (
            readcmd("hg", "log", "-r", ".", "--template", template, cwd=self.path)
            .splitlines()[0]
            .split(":")
        )
        distance = int(sdistance)
        rev = readcmd("hg", "id", "-i", cwd=self.path).removesuffix("+")
        return HGInfo(
            distance=distance,
            rev=rev,
            revision=revision,
        )


@dataclass
class HGInfo:
    build_date: datetime = field(init=False, default=BUILD_DATE)
    distance: int
    rev: str
    revision: str
    vcs: str = field(init=False, default="h")
    vcs_name: str = field(init=False, default="hg")

    def save(self, path: Path) -> None:
        with path.open("w", encoding="utf-8") as fp:
            json.dump(asdict(self), fp, default=str)


def zip_git(repo: Path, zipfile: Path) -> None:
    runcmd("git", "gc", "--aggressive", "--prune=now", cwd=repo)
    zipdir(repo, zipfile)
