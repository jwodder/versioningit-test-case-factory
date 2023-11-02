from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase
from factory.util import write_json


class TestCase(ZipCase):
    NAME = "custom-format-dirty"
    PATH = Path("repos", "git")
    EXTRAS = [".json"]

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Some code")
        self.sync("0200-packaged")
        git.commit("Packaging")
        git.tag("v0.1.0")
        self.patch("0300-custom-format")
        self.patch("0300-dirt")
        git.zip()
        write_json(
            self.asset_path(".json"),
            {
                "version": "0.1.0+dirty",
                "next_version": "0.2.0",
            },
        )
