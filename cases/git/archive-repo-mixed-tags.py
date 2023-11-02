from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase
from factory.util import write_json


class TestCase(ZipCase):
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
        self.patch("0300-archive-tags")
        git.commit("Switch to git-archive")
        self.patch("0300-feature")
        git.commit("Add a feature")
        git.tag("v0.2.0")
        git.zip()
        write_json(
            self.asset_path(".json"),
            {
                "version": "0.2.0",
                "next_version": "0.3.0",
            },
        )
