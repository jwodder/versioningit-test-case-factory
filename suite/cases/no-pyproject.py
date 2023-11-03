from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    """Produces a Python project that does not use :file:`pyproject.toml`"""

    NAME = "no-pyproject"
    PATH = Path("repos")

    def build(self) -> None:
        git = self.git()
        self.sync("0200-no-pyproject")
        git.commit("Packaging with setup.py")
        git.tag("v0.1.0")
        git.zip()
