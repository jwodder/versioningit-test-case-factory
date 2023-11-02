from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    NAME = "no-versioningit"
    PATH = Path("repos")

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Code")
        git.tag("v0.0.0")
        self.sync("0200-no-versioningit")
        git.commit("Packaging without versioningit")
        git.zip()
