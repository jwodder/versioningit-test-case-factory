from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase
from factory.util import write_json


class TestCase(ZipCase):
    NAME = "write-py"
    PATH = Path("repos", "git")
    EXTRAS = [".json"]

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Some code")
        self.sync("0200-packaged")
        git.commit("Packaging")
        git.tag("v0.1.0")
        self.patch("0300-write-py")
        git.commit("Write version to .py file")
        git.zip()
        info = git.get_info()
        write_json(
            self.asset_path(".json"),
            {
                "version": f"0.1.0.post1+g{info.rev}",
                "next_version": "0.2.0",
                "files": [
                    {
                        "sdist_path": "src/mypackage/_version.py",
                        "wheel_path": "mypackage/_version.py",
                        "contents": f'__version__ = "0.1.0.post1+g{info.rev}"\n',
                    }
                ],
            },
        )
