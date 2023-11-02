#!/usr/bin/env python3
from __future__ import annotations
import argparse
from collections.abc import Sequence
from dataclasses import dataclass
import logging
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tempfile

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

    def cmp_sdists(self, name: str, old_sdist: Path, new_sdist: Path) -> None:
        shutil.unpack_archive(old_sdist, self.old_dir)
        shutil.unpack_archive(new_sdist, self.new_dir)
        (old_src,) = self.old_dir.iterdir()
        (new_src,) = self.old_dir.iterdir()
        self.diff(name, old_src, new_src, exclude=["mypackage.egg-info", "PKG-INFO"])
        shutil.rmtree(self.old_dir)
        shutil.rmtree(self.new_dir)

    def cmp_zips(self, name: str, old_zip: Path, new_zip: Path) -> None:
        shutil.unpack_archive(old_zip, self.old_dir)
        shutil.unpack_archive(new_zip, self.new_dir)
        self.diff(name, self.old_dir, self.new_dir, exclude=[".git", ".hg"])
        shutil.rmtree(self.old_dir)
        shutil.rmtree(self.new_dir)

    def diff(
        self, name: str, old_path: Path, new_path: Path, exclude: Sequence[str] = ()
    ) -> None:
        log.info("Comparing %s ...", name)
        cmd = ["diff", "-Naur"]
        for ex in exclude:
            cmd.append("-x")
            cmd.append(ex)
        r = subprocess.run(
            [*cmd, "--", str(old_path), str(new_path)],
            stdout=subprocess.PIPE,
            text=True,
        )
        if r.returncode == 0:
            log.info("%s: OK", name)
        elif r.returncode == 1:
            log.info("%s: DIFF", name)
            (self.diffdir / PurePosixPath(name).name).write_text(r.stdout)
        else:
            raise RuntimeError(f"diff command exited with {r.returncode}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--diff-dir", type=Path, default="diffs")
    parser.add_argument("versioningit_repo", type=Path)
    args = parser.parse_args()
    logging.basicConfig(
        format="%(asctime)s [%(levelname)-8s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
    )
    with tempfile.TemporaryDirectory() as tmpdir:
        comparer = Comparer(workdir=Path(tmpdir), diffdir=args.diff_dir)
        test_data = args.versioningit_repo / "test" / "data"
        target = Path(__file__).parent.parent / "target"
        (old_sdist,) = test_data.glob("*.tar.gz")
        (new_sdist,) = target.glob("*.tar.gz")
        comparer.cmp_sdists(old_sdist.name, old_sdist, new_sdist)
        for old_zip in (test_data / "repos").rglob("*.zip"):
            name = old_zip.relative_to(test_data)
            comparer.cmp_zips(name.as_posix(), old_zip, target / name)


if __name__ == "__main__":
    main()
