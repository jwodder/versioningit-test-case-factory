from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    """
    Produces a Git repository in which versioningit is configured to use a
    custom ``tag2version`` method imported from a module in the package
    """

    NAME = "custom-method-src"
    PATH = Path("repos", "git")
    EXTRAS = [".json"]

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Some code")
        self.sync("0200-packaged")
        git.commit("Packaging")
        git.tag("rel_0_1_0")
        self.sync("0300-custom-method-src")
        git.commit("Use a custom method inside package for tag2version")
        git.zip()
        info = git.get_info()
        self.json(
            {
                "version": f"0.1.0.post1+g{info.rev}",
                "next_version": "0.2.0",
                "local_modules": ["mypackage.mymethods", "mypackage"],
            },
        )
