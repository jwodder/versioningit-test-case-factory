from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    """
    Produces a Mercurial repository in which versioningit is configured to
    exclude all tags, leading to an error
    """

    NAME = "hg-no-tag"
    PATH = Path("repos", "hg-errors")
    EXTRAS = [".json"]

    def build(self) -> None:
        hg = self.hg()
        self.sync("0200-hg-packaged")
        hg.commit("Packaging")
        hg.tag("0.1.0")
        self.sync("0300-hg-pattern")
        hg.commit("Set vcs.pattern")
        hg.tag("0.2.0")
        hg.zip()
        self.json(
            {
                "type": "NoTagError",
                "message": "No latest tag in Mercurial repository (pattern = 're:^v')",
            },
        )
