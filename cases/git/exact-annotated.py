from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase
from factory.util import write_json


class TestCase(ZipCase):
    NAME = "exact-annotated"
    PATH = Path("repos", "git")
    EXTRAS = [".json"]

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Some code")
        self.sync("0200-packaged")
        git.commit("Packaging")
        git.tag("v0.1.0", message="v0.1.0")
        self.patch("0300-feature")
        git.commit("Add a feature")
        git.zip()
        write_json(
            self.asset_path(".json"),
            {
                "version": "0.1.0",
                "next_version": "0.2.0",
            },
        )
