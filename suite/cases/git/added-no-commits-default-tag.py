from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    """
    Produces a Git repository in which no commits have been made but
    ``vcs.default-tag`` is set
    """

    NAME = "added-no-commits-default-tag"
    PATH = Path("repos", "git")
    EXTRAS = [".json"]

    def build(self) -> None:
        git = self.git()
        self.sync("0300-default-tag")
        git.rungit("add", ".")
        git.zip()
        self.json({"version": "0.0.0+d20380119", "next_version": "0.1.0"})
