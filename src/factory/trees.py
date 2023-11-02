from __future__ import annotations
from dataclasses import dataclass
import logging
from pathlib import Path
import shutil
import subprocess
from iterpath import SELECT_VCS, SELECT_VCS_DIRS, iterpath
from pydantic import BaseModel
from .util import rm_to_root, runcmd

log = logging.getLogger()


class PatchDef(BaseModel):
    before: str
    after: str


@dataclass
class Trees:
    tree_dir: Path
    patch_dir: Path
    patchdefs: dict[str, PatchDef]

    def __post_init__(self) -> None:
        self.patch_dir.mkdir(parents=True, exist_ok=True)
        for name, pdef in self.patchdefs.items():
            if not (self.tree_dir / pdef.before).is_dir():
                raise RuntimeError(
                    f"Tree {pdef.before} needed for patch {name} does not exist"
                )
            if not (self.tree_dir / pdef.after).is_dir():
                raise RuntimeError(
                    f"Tree {pdef.after} needed for patch {name} does not exist"
                )

    def apply_patch(self, dirpath: Path, patch: str) -> None:
        with self.get_patch(patch).open(encoding="utf-8") as fp:
            log.debug("Applying patch %s to %s", patch, dirpath)
            runcmd("patch", "-p1", cwd=dirpath, stdin=fp)
        # Delete empty files and afterwards empty directories:
        # (Note that doing the first part through `patch -E` isn't standard)
        with iterpath(dirpath, dirs=False, exclude_dirs=SELECT_VCS_DIRS) as ip:
            emptyfiles = [p for p in ip if p.stat().st_size == 0]
        for p in emptyfiles:
            rm_to_root(p, dirpath)

    def get_patch(self, patch: str) -> Path:
        patchfile = self.patch_dir / f"{patch}.diff"
        if not patchfile.exists():
            log.info("Creating patch %s", patch)
            pdef = self.patchdefs[patch]
            r = runcmd(
                "diff",
                "-Naur",
                pdef.before,
                pdef.after,
                stdout=subprocess.PIPE,
                text=True,
                cwd=self.tree_dir,
                check=False,
            )
            if r.returncode == 0:
                raise RuntimeError(f"Patch {patch} is empty")
            elif r.returncode == 1:
                patchfile.write_text(r.stdout, encoding="utf-8")
            else:
                r.check_returncode()
        return patchfile

    def sync_dir(self, dirpath: Path, tree: str) -> None:
        """
        Make the contents of ``dirpath`` identical to those of the given tree,
        preserving any VCS files already present
        """
        log.debug("Purging %s before applying tree %s ...", dirpath, tree)
        with iterpath(dirpath, dirs=False, exclude=SELECT_VCS) as ip:
            to_delete = list(ip)
        for p in to_delete:
            rm_to_root(p, dirpath)
        log.debug("Applying tree %s to %s ...", tree, dirpath)
        treedir = self.tree_dir / tree
        with iterpath(treedir, dirs=False, return_relative=True) as ip:
            for p in ip:
                src = treedir / p
                dest = dirpath / p
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
