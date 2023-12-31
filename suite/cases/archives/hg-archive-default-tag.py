from __future__ import annotations
from pathlib import Path
import shutil
from factory.case import ZipCase
from factory.util import runcmd, zipdir

BASE = "hg-default-tag"


class TestCase(ZipCase):
    """
    Produces an archive of a Mercurial repository without any tags but with
    ``vcs.default-tag`` set
    """

    NAME = "hg-archive-default-tag"
    PATH = Path("repos", "archives")
    DEPENDENCIES = [BASE]
    EXTRAS = [".json"]

    def build(self) -> None:
        dep = self.dependencies[BASE]
        assert isinstance(dep, ZipCase)
        runcmd("hg", "archive", self.mkwork(), cwd=dep.work_dir)
        zipdir(self.work_dir, self.zipfile)
        shutil.copy(dep.asset_path(".json"), self.asset_path(".json"))
