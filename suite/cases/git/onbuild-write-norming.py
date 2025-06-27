from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    """
    Produces a Git repository in which versioningit produces a non-normalized version and
    both the ``onbuild`` and ``write`` steps are configured to use both the
    normalized & un-normalized versions.
    """

    ID = "onbuild-write-norming"
    NAME = "onbuild-write-norming"
    PATH = Path("repos", "git")
    EXTRAS = [".json"]

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Some code")
        self.sync("0200-packaged")
        git.commit("Packaging")
        git.tag("v0.1.0")
        self.sync("0300-onbuild")
        git.commit("Use onbuild")
        self.sync("0400-onbuild-write-norming")
        with (self.work_dir / ".gitignore").open("a", encoding="utf-8") as fp:
            print("src/mypackage/_version.py", file=fp)
        git.commit("Also use write and a non-normalized version")
        git.zip()
        self.json(
            {
                "version": "0.1.0-r2",
                "pkg_version": "0.1.0.post2",
                "next_version": "0.2.0",
                "files": [
                    {
                        "sdist_path": "src/mypackage/_version.py",
                        "wheel_path": "mypackage/_version.py",
                        "contents": '__raw_version__ = "0.1.0-r2"\n__version__ = "0.1.0.post2"\n',
                    },
                    {
                        "sdist_path": "src/mypackage/__init__.py",
                        "wheel_path": "mypackage/__init__.py",
                        "in_project": False,
                        "contents": '""" A test package """\n\n__raw_version__ = "0.1.0-r2"\n__version__ = "0.1.0.post2"\n',
                    },
                ],
            },
        )
