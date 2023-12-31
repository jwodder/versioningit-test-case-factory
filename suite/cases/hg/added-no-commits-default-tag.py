from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    """
    Produces a Mercurial repository in which no commits have been made but
    ``vcs.default-tag`` is set
    """

    NAME = "added-no-commits-default-tag"
    PATH = Path("repos", "hg")
    EXTRAS = [".json"]

    def build(self) -> None:
        hg = self.hg()
        self.sync("0300-hg-default-tag")
        hg.runhg("add")
        hg.zip()
        self.json(
            {
                "version": "0.0.0+d20380119",
                "next_version": "0.1.0",
            },
        )
