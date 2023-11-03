from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase
from factory.util import zipdir


class TestCase(ZipCase):
    """Produces a Python project that is not managed by a VCS"""

    NAME = "no-git"
    PATH = Path("repos")

    def build(self) -> None:
        self.sync("0200-packaged")
        zipdir(self.work_dir, self.zipfile)
