from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    NAME = "write-encoding"
    PATH = Path("repos", "git")
    EXTRAS = [".json"]

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Some code")
        self.sync("0200-packaged")
        git.commit("Packaging")
        git.tag("v0.1.0")
        self.patch("0300-write-encoding")
        with (self.work_dir / ".gitignore").open("a", encoding="utf-8") as fp:
            print("src/mypackage/_version.py", file=fp)
        git.commit("Write version to .py file")
        git.zip()
        info = git.get_info()
        self.json(
            {
                "version": f"0.1.0.post1+g{info.rev}",
                "next_version": "0.2.0",
                "files": [
                    {
                        "sdist_path": "src/mypackage/_version.py",
                        "wheel_path": "mypackage/_version.py",
                        "encoding": "cp1252",
                        "contents": f'__version__ = "\u20140.1.0.post1+g{info.rev}\u2014"\n',
                    }
                ],
            },
        )
