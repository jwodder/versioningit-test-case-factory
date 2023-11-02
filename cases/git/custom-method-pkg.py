from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase
from factory.util import write_json


class TestCase(ZipCase):
    NAME = "custom-method-pkg"
    PATH = Path("repos", "git")
    EXTRAS = [".json"]

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Some code")
        self.sync("0200-packaged")
        git.commit("Packaging")
        git.tag("rel_0_1_0")
        self.patch("0300-custom-method-src")
        git.commit("Use a custom method inside package for tag2version")
        self.patch("0300-custom-method-pkg")
        git.commit("Import custom method from package")
        git.zip()
        info = git.get_info()
        write_json(
            self.asset_path(".json"),
            {
                "version": f"0.1.0.post2+g{info.rev}",
                "next_version": "0.2.0",
                "local_modules": ["mypackage.mymethods", "mypackage"],
            },
        )
