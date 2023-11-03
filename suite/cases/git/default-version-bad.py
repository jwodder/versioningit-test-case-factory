from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


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
        self.sync("0300-default-version")
        git.commit("Use default-version")
        self.sync("0400-default-version-bad")
        git.commit("Use a non-PEP 440 default-version")
        git.zip()
        self.json(
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
        self.marks("describe_exclude", "oldsetup")
