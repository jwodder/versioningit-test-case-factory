from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase
from factory.util import write_json


class TestCase(ZipCase):
    NAME = "added-no-commits-default-tag"
    PATH = Path("repos", "hg")
    EXTRAS = [".json"]

    def build(self) -> None:
        hg = self.hg()
        self.sync("0300-hg-default-tag")
        hg.runhg("add")
        hg.zip()
        write_json(
            self.asset_path(".json"),
            {
                "version": "0.0.0+d20380119",
                "next_version": "0.1.0",
            },
        )
