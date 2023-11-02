from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase
from factory.util import write_json


class TestCase(ZipCase):
    NAME = "default-tag"
    PATH = Path("repos", "hg")
    EXTRAS = [".json"]

    def build(self) -> None:
        hg = self.hg()
        self.sync("0100-code")
        hg.commit("Some code")
        self.sync("0200-hg-packaged")
        hg.commit("Packaging")
        self.patch("0300-hg-default-tag")
        hg.commit("Set default-tag")
        hg.zip()
        info = hg.get_info()
        write_json(
            self.asset_path(".json"),
            {
                "version": f"0.0.0.post2+h{info.rev}",
                "next_version": "0.1.0",
            },
        )
