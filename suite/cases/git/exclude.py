from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    """
    Produces a Git repository in which the most recent tag is excluded by the
    ``vcs.exclude`` setting
    """

    NAME = "exclude"
    PATH = Path("repos", "git")
    EXTRAS = [".json", ".fields.json", ".marks"]

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Some code")
        self.sync("0200-packaged")
        git.commit("Packaging")
        git.tag("0.1.0")
        self.sync("0300-exclude")
        git.commit("Set vcs.exclude")
        git.tag("v0.2.0")
        git.zip()
        info = git.get_info(exclude=["v*"])
        self.json(
            {
                "version": f"0.1.0.post1+g{info.rev}",
                "next_version": "0.2.0",
            },
        )
        info.save(self.asset_path(".fields.json"))
        self.marks("describe_exclude")
