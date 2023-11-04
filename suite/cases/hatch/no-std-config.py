from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    """
    Produces a Git repository using Hatch in which there is
    ``[tool.versioningit]`` table and the ``[tool.hatch.version]`` table is
    trivial
    """

    NAME = "no-std-config"
    PATH = Path("repos", "hatch")
    EXTRAS = [".json"]

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Some code")
        self.sync("0200-hatch-packaged")
        git.commit("Packaging with hatch")
        git.tag("v0.1.0")
        self.sync("0300-hatch-no-tool")
        git.commit("Remove [tool.versioningit] table")
        git.zip()
        info = git.get_info()
        self.json(
            {
                "version": f"0.1.0.post1+g{info.rev}",
                "next_version": "0.2.0",
            },
        )
