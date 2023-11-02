from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase
from factory.util import write_json


class TestCase(ZipCase):
    NAME = "pattern"
    PATH = Path("repos", "hg")
    EXTRAS = [".json"]

    def build(self) -> None:
        hg = self.hg()
        self.sync("0100-code")
        hg.commit("Some code")
        self.sync("0200-hg-packaged")
        hg.commit("Packaging")
        hg.tag("v0.1.0")
        self.patch("0300-hg-feature")
        hg.commit("Add a feature")
        self.patch("0300-hg-pattern")
        hg.commit("Set vcs.pattern")
        hg.tag("0.2.0")
        hg.zip()
        info = hg.get_info()
        write_json(
            self.asset_path(".json"),
            {
                "version": f"0.1.0.post4+h{info.rev}",
                "next_version": "0.2.0",
            },
        )
