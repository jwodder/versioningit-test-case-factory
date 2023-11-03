from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    """
    Produces a Git repository in which the most recent tag is filtered out by
    the ``vcs.match`` setting
    """

    NAME = "match"
    PATH = Path("repos", "git")
    EXTRAS = [".json", ".fields.json"]

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Some code")
        self.sync("0200-packaged")
        git.commit("Packaging")
        git.tag("v0.1.0")
        self.sync("0300-match")
        git.commit("Set vcs.match")
        git.tag("0.2.0")
        git.zip()
        info = git.get_info(match=["v*"])
        self.json({"version": f"0.1.0.post1+g{info.rev}", "next_version": "0.2.0"})
        info.save(self.asset_path(".fields.json"))
