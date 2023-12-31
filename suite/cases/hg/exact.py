from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    """
    Produces a Mercurial repository in which the working directory has been
    updated to point to a tag.

    (In Mercurial, creating a tag creates a commit.)
    """

    ID = "hg-exact"
    NAME = "exact"
    PATH = Path("repos", "hg")
    EXTRAS = [".json", ".fields.json"]

    def build(self) -> None:
        hg = self.hg()
        self.sync("0100-code")
        hg.commit("Some code")
        self.sync("0200-hg-packaged")
        hg.commit("Packaging")
        hg.tag("v0.1.0")
        hg.runhg("update", "-r", "v0.1.0")
        hg.zip()
        self.json(
            {
                "version": "0.1.0",
                "next_version": "0.2.0",
            },
        )
        hg.get_info().save(self.asset_path(".fields.json"))
