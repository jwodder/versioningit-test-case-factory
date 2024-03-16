from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    """
    Produces a Git repository without any tags but with ``default-version`` set
    to a non-PEP 440 version
    """

    NAME = "default-version-bad"
    PATH = Path("repos", "git")
    EXTRAS = [".json", ".marks"]

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Some code")
        self.sync("0200-packaged")
        git.commit("Packaging")
        self.sync("0300-default-version-bad")
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
                        "message": "Falling back to default-version",
                    },
                    {
                        "level": "WARNING",
                        "message": "Final version '1.1.1m' is not PEP 440-compliant",
                    },
                ],
            },
        )
        self.marks("oldsetup")
