from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase
from factory.util import runcmd
from factory.vcs import zip_git


class TestCase(ZipCase):
    NAME = "shallow"
    PATH = Path("repos")

    def build(self) -> None:
        runcmd(
            "git",
            "clone",
            "--depth",
            "1",
            "https://github.com/jwodder/versioningit-test",
            self.mkwork(),
        )
        zip_git(self.work_dir, self.zipfile)
