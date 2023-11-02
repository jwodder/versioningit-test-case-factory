from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase
from factory.util import write_json


class TestCase(ZipCase):
    NAME = "default-version"
    PATH = Path("repos", "git")
    EXTRAS = [".json", ".marks"]

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Some code")
        self.sync("0200-packaged")
        git.commit("Packaging")
        git.tag("v0.1.0")
        self.patch("0300-default-version")
        git.commit("Use default-version")
        git.zip()
        write_json(
            self.asset_path(".json"),
            {
                "version": "0.0.0+error",
                "next_version": {
                    "type": "NoTagError",
                    "message": "`git describe` could not find a tag",
                },
                "logmsgs": [
                    {
                        "level": "ERROR",
                        "message": "NoTagError: `git describe` could not find a tag",
                    },
                    {
                        "level": "INFO",
                        "message": "Falling back to tool.versioningit.default-version",
                    },
                ],
            },
        )
        self.asset_path(".marks").write_text("describe_exclude\n")
