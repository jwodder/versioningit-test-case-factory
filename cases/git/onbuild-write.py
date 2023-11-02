from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase
from factory.util import write_json


class TestCase(ZipCase):
    NAME = "onbuild-write"
    PATH = Path("repos", "git")
    EXTRAS = [".json"]

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Some code")
        self.sync("0200-packaged")
        git.commit("Packaging")
        git.tag("v0.1.0")
        self.patch("0300-feature")
        git.commit("Add a feature")
        self.patch("0400-onbuild")
        git.commit("Use onbuild")
        self.patch("0500-add-write-to-onbuild")
        git.commit("Also use write")
        git.zip()
        info = git.get_info()
        write_json(
            self.asset_path(".json"),
            {
                "version": f"0.1.0.post3+g{info.rev}",
                "next_version": "0.2.0",
                "files": [
                    {
                        "sdist_path": "src/mypackage/_version.py",
                        "wheel_path": "mypackage/_version.py",
                        "contents": f'__version__ = "0.1.0.post3+g{info.rev}"\n',
                    },
                    {
                        "sdist_path": "src/mypackage/__init__.py",
                        "wheel_path": "mypackage/__init__.py",
                        "in_project": False,
                        "contents": f'""" A test package """\n\n__version__ = "0.1.0.post3+g{info.rev}"\n__author__ = "John Thorvald Wodder II"\n__author_email__ = "mypackage@varonathe.org"\n__license__ = "MIT"\n',
                    },
                ],
            },
        )
