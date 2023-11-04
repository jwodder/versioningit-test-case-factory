from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    """
    Produces a Git repository using Hatch in which the most recent commit is
    tagged with a lightweight tag
    """

    NAME = "exact"
    PATH = Path("repos", "hatch")
    EXTRAS = [".json"]

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Some code")
        self.sync("0200-hatch-packaged")
        git.commit("Packaging with hatch")
        git.tag("v0.1.0")
        git.zip()
        self.json({"version": "0.1.0", "next_version": "0.2.0"})
