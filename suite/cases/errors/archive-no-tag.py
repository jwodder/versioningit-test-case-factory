from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    """
    Produces a Git repository in which versioningit is configured to use the
    "git-archive" method and all tags are excluded by the ``vcs.exclude``
    setting
    """

    NAME = "archive-no-tag"
    PATH = Path("repos", "errors")
    EXTRAS = [".json", ".marks"]

    def build(self) -> None:
        git = self.git()
        self.sync("0200-packaged")
        git.commit("Packaging")
        git.tag("v0.1.0", message="Version 0.1.0")
        self.sync("0300-archive-exclude")
        git.commit("Switch to git-archive")
        git.tag("v0.2.0", message="Version 0.2.0")
        git.zip()
        self.json(
            {
                "type": "NoTagError",
                "message": "`git describe --long --dirty --always '--exclude=v*'` could not find a tag",
            },
        )
        self.marks("describe_exclude")
