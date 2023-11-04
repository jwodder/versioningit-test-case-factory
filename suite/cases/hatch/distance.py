from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    """
    Produces a Git repository using Hatch in which one or more commits have
    been made since the most recent tag
    """

    NAME = "distance"
    PATH = Path("repos", "hatch")
    EXTRAS = [".json"]

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Some code")
        self.sync("0200-hatch-packaged")
        git.commit("Packaging with hatch")
        git.tag("v0.1.0")
        self.sync("0300-hatch-feature")
        git.commit("Add a feature")
        git.zip()
        info = git.get_info()
        self.json(
            {
                "version": f"0.1.0.post1+g{info.rev}",
                "next_version": "0.2.0",
            },
        )
