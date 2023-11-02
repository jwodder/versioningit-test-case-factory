from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase
from factory.util import write_json


class TestCase(ZipCase):
    NAME = "exclude"
    PATH = Path("repos", "git")
    EXTRAS = [".json", ".marks"]

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Some code")
        self.sync("0200-packaged")
        git.commit("Packaging")
        git.tag("0.1.0")
        self.patch("0300-feature")
        git.commit("Add a feature")
        self.patch("0300-exclude")
        git.commit("Set vcs.exclude")
        git.tag("v0.2.0")
        git.zip()
        info = git.get_info()
        write_json(
            self.asset_path(".json"),
            {
                "version": f"0.1.0.post2+g{info.rev}",
                "next_version": "0.2.0",
            },
        )
        self.asset_path(".marks").write_text("describe_exclude\n")
