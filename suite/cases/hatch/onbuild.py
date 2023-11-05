from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    """Produces a Git repository using Hatch that uses the ``onbuild`` step"""

    NAME = "onbuild"
    PATH = Path("repos", "hatch")
    EXTRAS = [".json"]

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Some code")
        self.sync("0200-hatch-packaged")
        git.commit("Packaging with Hatch")
        git.tag("v0.1.0")
        self.sync("0300-hatch-onbuild")
        git.commit("Use onbuild")
        git.zip()
        info = git.get_info()
        self.json(
            {
                "version": f"0.1.0.post1+g{info.rev}",
                "next_version": "0.2.0",
                "files": [
                    {
                        "sdist_path": "src/mypackage/__init__.py",
                        "wheel_path": "mypackage/__init__.py",
                        "in_project": False,
                        "contents": f'""" A test package """\n\n__version__ = "0.1.0.post1+g{info.rev}"\n',
                    }
                ],
            },
        )
