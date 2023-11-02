from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    NAME = "distance-dirty"
    PATH = Path("repos", "hg")
    EXTRAS = [".json", ".fields.json"]

    def build(self) -> None:
        hg = self.hg()
        self.sync("0100-code")
        hg.commit("Some code")
        self.sync("0200-hg-packaged")
        hg.commit("Packaging")
        hg.tag("v0.1.0")
        self.patch("0300-hg-dirt")
        hg.runhg("addremove")
        hg.zip()
        info = hg.get_info()
        self.json(
            {
                "version": f"0.1.0.post1+h{info.rev}.d20380119",
                "next_version": "0.2.0",
            },
        )
        info.save(self.asset_path(".fields.json"))
