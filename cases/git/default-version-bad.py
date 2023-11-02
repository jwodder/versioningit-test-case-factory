from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase
from factory.util import write_json


class TestCase(ZipCase):
    NAME = "default-version-bad"
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
        self.patch("0400-default-version-bad")
        git.commit("Use a non-PEP 440 default-version")
        git.zip()
        write_json(
            self.asset_path(".json"),
            {
                "version": "1.1.1m",
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
                    {
                        "level": "WARNING",
                        "message": "Final version '1.1.1m' is not PEP 440-compliant",
                    },
                ],
            },
        )
        self.asset_path(".marks").write_text("describe_exclude\noldsetup\n")
