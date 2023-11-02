from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    NAME = "archive-repo-match"
    PATH = Path("repos", "git")
    EXTRAS = [".json"]

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Some code")
        self.sync("0200-packaged")
        git.commit("Packaging")
        git.tag("v0.1.0", message="Version 0.1.0")
        self.patch("0300-archive-match")
        git.commit("Switch to git-archive")
        self.patch("0300-feature")
        git.commit("Add a feature")
        git.tag("0.2.0", message="Version 0.2.0")
        git.zip()
        info = git.get_info()
        self.json(
            {
                "version": f"0.1.0.post2+g{info.rev}",
                "next_version": "0.2.0",
            },
        )
