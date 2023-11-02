from __future__ import annotations
import logging
from pathlib import Path
import shlex
import subprocess
from typing import Any
from zipfile import ZipFile
from iterpath import SelectGlob, iterpath

log = logging.getLogger(__name__)


def runcmd(*args: str | Path, **kwargs: Any) -> subprocess.CompletedProcess:
    argstrs = [str(a) for a in args]
    log.debug("Running: %s", " ".join(map(shlex.quote, argstrs)))
    kwargs.setdefault("check", True)
    return subprocess.run(argstrs, **kwargs)


def readcmd(*args: str | Path, **kwargs: Any) -> str:
    kwargs["stdout"] = subprocess.PIPE
    kwargs["text"] = True
    r = runcmd(*args, **kwargs)
    assert isinstance(r.stdout, str)
    return r.stdout.strip()


def zipdir(dirpath: Path, zipfile: Path) -> None:
    log.debug("Creating zipfile %s of %s", zipfile, dirpath)
    with ZipFile(zipfile, mode="w") as zf:
        with iterpath(
            dirpath,
            return_relative=True,
            sort=True,
            exclude_files=SelectGlob("*.sample"),
        ) as ip:
            for p in ip:
                log.debug("Adding %s to zipfile", p)
                zf.write(dirpath / p, p)


def rm_to_root(filepath: Path, rootdir: Path) -> None:
    """
    Unlink the file ``filepath`` and all parent directories recursively, as
    long as each such directory is empty (after deleting the previous node) and
    not equal to ``rootdir``
    """
    filepath.unlink()
    d = filepath.parent
    while d != rootdir and not any(d.iterdir()):
        d.rmdir()
        d = d.parent
