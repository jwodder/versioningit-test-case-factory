from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    """
    Produces a Git repository with ``default-version`` set and with the
    ``onbuild`` and ``write`` steps enabled.

    Unlike ``default-version`` and ``default-version-bad``, this test case
    creates a tag that is filtered out by the project's ``vcs.match`` setting
    in order to test that versioningit does the right thing when all tags are
    filtered out.
    """

    NAME = "default-version-onbuild-write"
    PATH = Path("repos", "git")
    EXTRAS = [".json"]

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Some code")
        self.sync("0200-packaged")
        git.commit("Packaging")
        git.tag("0.1.0")
        self.sync("0300-default-version-onbuild-write")
        with (self.work_dir / ".gitignore").open("a", encoding="utf-8") as fp:
            print("src/mypackage/_version.py", file=fp)
        git.commit("Use write, onbuild, and default-version")
        git.zip()
        self.json(
            {
                "version": "0.0.0+error",
                "next_version": {
                    "type": "NoTagError",
                    "message": "`git describe --long --dirty --always --tags '--match=v*'` could not find a tag",
                },
                "logmsgs": [
                    {
                        "level": "ERROR",
                        "message": "NoTagError: `git describe --long --dirty --always --tags '--match=v*'` could not find a tag",
                    },
                    {
                        "level": "INFO",
                        "message": "Falling back to default-version",
                    },
                ],
                "files": [
                    {
                        "sdist_path": "src/mypackage/_version.py",
                        "wheel_path": "mypackage/_version.py",
                        "contents": '__version__ = "0.0.0+error"\n__version_tuple__ = (0, 0, 0, "+error")\n',
                    },
                    {
                        "sdist_path": "src/mypackage/__init__.py",
                        "wheel_path": "mypackage/__init__.py",
                        "in_project": False,
                        "contents": '""" A test package """\n\n__version__ = "0.0.0+error"\n__version_tuple__ = (0, 0, 0, "+error")\n',
                    },
                ],
            },
        )
