from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    ID = "git-archive-repo-mixed-tags"
    NAME = "archive-repo-mixed-tags"
    PATH = Path("repos", "git")
    EXTRAS = [".json"]

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Some code")
        self.sync("0200-packaged")
        git.commit("Packaging")
        git.tag("v0.1.0", message="Version 0.1.0")
        self.sync("0300-archive-tags")
        git.commit("Switch to git-archive")
        git.tag("v0.2.0")
        git.zip()
        self.json(
            {
                "version": "0.2.0",
                "next_version": "0.3.0",
            },
        )
