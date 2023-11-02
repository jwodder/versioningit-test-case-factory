from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    NAME = "default-tag"
    PATH = Path("repos", "git")
    EXTRAS = [".json", ".fields.json"]

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Some code")
        self.sync("0200-packaged")
        git.commit("Packaging")
        self.patch("0300-default-tag")
        git.commit("Set default-tag")
        git.zip()
        info = git.get_info()
        self.json({"version": f"0.0.0.post2+g{info.rev}", "next_version": "0.1.0"})
        info.save(self.asset_path(".fields.json"))
