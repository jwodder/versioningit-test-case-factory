from __future__ import annotations
from dataclasses import dataclass
import logging
from pathlib import Path
import shutil
from iterpath import SELECT_VCS, iterpath
from .util import rm_to_root

log = logging.getLogger()


@dataclass
class Trees:
    tree_dir: Path

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
                if p == Path(".description"):
                    continue
                src = treedir / p
                dest = dirpath / p
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dest)
