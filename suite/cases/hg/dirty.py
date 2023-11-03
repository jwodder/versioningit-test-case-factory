from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    NAME = "dirty"
    PATH = Path("repos", "hg")
    EXTRAS = [".json"]

    def build(self) -> None:
        hg = self.hg()
        self.sync("0100-code")
        hg.commit("Some code")
        self.sync("0200-hg-packaged")
        hg.commit("Packaging")
        hg.tag("v0.1.0")
        hg.runhg("update", "-r", "v0.1.0")
        self.dirty()
        hg.runhg("addremove")
        hg.zip()
        self.json({"version": "0.1.0+d20380119", "next_version": "0.2.0"})
