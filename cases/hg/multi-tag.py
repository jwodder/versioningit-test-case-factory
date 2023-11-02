from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    NAME = "multi-tag"
    PATH = Path("repos", "hg")
    EXTRAS = [".json"]

    def build(self) -> None:
        hg = self.hg()
        self.sync("0100-code")
        hg.commit("Some code")
        self.sync("0200-hg-packaged")
        hg.commit("Packaging")
        hg.tag("v0.1.0")
        hg.runhg("tag", "-r", "v0.1.0", "vextra")
        hg.zip()
        info = hg.get_info()
        self.json({"version": f"0.1.0.post2+h{info.rev}", "next_version": "0.2.0"})
