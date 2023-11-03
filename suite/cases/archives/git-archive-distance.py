from __future__ import annotations
from pathlib import Path
import shutil
from factory.case import ZipCase
from factory.util import runcmd

BASE = "git-archive-repo"


class TestCase(ZipCase):
    """
    Produces an archive of a Git repository in which one or more commits have
    been made since the most recent tag
    """

    NAME = "git-archive-distance"
    PATH = Path("repos", "archives")
    DEPENDENCIES = [BASE]
    EXTRAS = [".json"]

    def build(self) -> None:
        dep = self.dependencies[BASE]
        assert isinstance(dep, ZipCase)
        runcmd(
            "git",
            "archive",
            "--format=zip",
            "-o",
            self.zipfile.absolute(),
            "HEAD",
            cwd=dep.work_dir,
        )
        shutil.copy(dep.asset_path(".json"), self.asset_path(".json"))
