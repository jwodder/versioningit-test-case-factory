from __future__ import annotations
from dataclasses import dataclass
import logging
from pathlib import Path
import shutil
import subprocess
from .util import runcmd

log = logging.getLogger()


@dataclass
class Comparer:
    workdir: Path
    diffdir: Path

    def __post_init__(self) -> None:
        self.diffdir.mkdir(parents=True, exist_ok=True)

    @property
    def old_dir(self) -> Path:
        return self.workdir / "old"

    @property
    def new_dir(self) -> Path:
        return self.workdir / "new"

    def __call__(self, name: str, old: Path, new: Path) -> None:
        shutil.unpack_archive(old, self.old_dir)
        shutil.unpack_archive(new, self.new_dir)
        if old.name.endswith(".tar.gz"):
            (old_dir,) = self.old_dir.iterdir()
            (new_dir,) = self.new_dir.iterdir()
        else:
            old_dir = self.old_dir
            new_dir = self.new_dir
        log.info("Comparing %s ...", name)
        r = runcmd(
            "diff",
            "-Naur",
            "-x",
            "*.egg-info",
            "-x",
            "PKG-INFO",
            "-x",
            ".git",
            "-x",
            ".hg",
            "--",
            old_dir,
            new_dir,
            stdout=subprocess.PIPE,
            text=True,
            check=False,
        )
        if r.returncode == 0:
            log.info("%s: OK", name)
        elif r.returncode == 1:
            log.info("%s: DIFF", name)
            p = self.diffdir / (name + ".diff")
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(r.stdout, encoding="utf-8")
        else:
            raise RuntimeError(f"diff command exited with {r.returncode}")
        shutil.rmtree(self.old_dir)
        shutil.rmtree(self.new_dir)
