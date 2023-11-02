from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    NAME = "template-fields-error"
    PATH = Path("repos", "errors")

    def build(self) -> None:
        git = self.git()
        self.sync("0200-packaged")
        git.commit("Packaging")
        git.tag("v0.1.0")
        self.sync("0300-template-fields-error")
        git.commit("Set us up for failure")
        git.zip()
        self.json(
            {
                "type": "InvalidVersionError",
                "message": "'0.2.0~1' is not a valid PEP 440 version",
            },
        )
