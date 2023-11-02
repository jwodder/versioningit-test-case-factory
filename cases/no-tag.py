from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase
from factory.util import write_json


class TestCase(ZipCase):
    NAME = "no-tag"
    PATH = Path("repos", "errors")
    EXTRAS = [".json", ".marks"]

    def build(self) -> None:
        git = self.git()
        self.sync("0200-packaged")
        git.commit("Packaging")
        git.tag("v0.1.0")
        self.sync("0300-exclude-all")
        git.commit("Induce an error")
        git.zip()
        write_json(
            self.asset_path(".json"),
            {"type": "NoTagError", "message": "`git describe` could not find a tag"},
        )
        self.asset_path(".marks").write_text("describe_exclude\n")
