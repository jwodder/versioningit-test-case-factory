from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    """
    Produces a Git repository using Hatch in which the ``write`` step is
    configured to produce a text file
    """

    NAME = "write-txt"
    PATH = Path("repos", "hatch")
    EXTRAS = [".json"]

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Some code")
        self.sync("0200-hatch-packaged")
        git.commit("Packaging with hatch")
        git.tag("v0.1.0")
        self.sync("0300-hatch-write-txt")
        with (self.work_dir / ".gitignore").open("a", encoding="utf-8") as fp:
            print("src/mypackage/version.txt", file=fp)
        git.commit("Write version to .txt file")
        git.zip()
        info = git.get_info()
        self.json(
            {
                "version": f"0.1.0.post1+g{info.rev}",
                "next_version": "0.2.0",
                "files": [
                    {
                        "sdist_path": "src/mypackage/version.txt",
                        "wheel_path": "mypackage/version.txt",
                        "contents": f"0.1.0.post1+g{info.rev}\n",
                    }
                ],
            },
        )
