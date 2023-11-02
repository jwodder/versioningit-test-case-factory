from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    NAME = "exact"
    PATH = Path("repos", "git")
    EXTRAS = [".json", ".fields.json", ".exclude.fields.json"]

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Some code")
        self.sync("0200-packaged")
        git.commit("Packaging")
        git.tag("v0.1.0")
        git.zip()
        self.json({"version": "0.1.0", "next_version": "0.2.0"})
        git.get_info().save(self.asset_path(".fields.json"))
        git.get_info(exclude=["v*"]).save(self.asset_path(".exclude.fields.json"))
