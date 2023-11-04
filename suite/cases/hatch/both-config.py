from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    """
    Produces a Git repository using Hatch in which versioningit has nontrivial
    configuration in both ``[tool.hatch.version]`` and ``[tool.versioningit]``
    """

    NAME = "both-config"
    PATH = Path("repos", "hatch")
    EXTRAS = [".json"]

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Some code")
        self.sync("0200-hatch-packaged")
        git.commit("Packaging with hatch")
        git.tag("v0.1.0")
        self.sync("0300-hatch-format-both")
        git.commit("Configure custom version formats via both tables")
        git.zip()
        info = git.get_info()
        self.json(
            {
                "version": f"0.2.0.dev1+g{info.rev}",
                "next_version": "0.2.0",
                "logmsgs": [
                    {
                        "level": "WARNING",
                        "message": (
                            "versioningit configuration found in both"
                            " [tool.hatch.version] and [tool.versioningit];"
                            " only using the former"
                        ),
                    }
                ],
            }
        )
