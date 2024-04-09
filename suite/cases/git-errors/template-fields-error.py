from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    """
    Produces a Python project where versioningit is configured to produce a
    non-PEP 440 version while also calculating the version tuple in PEP 440
    mode, resulting in an error
    """

    NAME = "template-fields-error"
    PATH = Path("repos", "git-errors")
    EXTRAS = [".json"]

    def build(self) -> None:
        git = self.git()
        self.sync("0200-packaged")
        git.commit("Packaging")
        git.tag("v0.1.0")
        self.sync("0300-template-fields-error")
        git.commit("Set us up for failure")
        git.zip()
        info = git.get_info()
        self.json(
            {
                "type": "InvalidVersionError",
                "message": f"'0.2.0~g{info.rev}' is not a valid PEP 440 version",
            },
        )
