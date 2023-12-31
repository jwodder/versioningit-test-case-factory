from __future__ import annotations
from collections.abc import Iterator
import logging
import os
from pathlib import Path
import re
import shutil
import tempfile
import click
from click_loglevel import LogLevel
from iterpath import SelectGlob, iterpath
from .compare import Comparer
from .factory import CaseFactory

log = logging.getLogger()


@click.group(context_settings={"help_option_names": ["-h", "--help"]})
@click.option(
    "-C",
    "--chdir",
    type=click.Path(exists=True, file_okay=False, dir_okay=True, path_type=Path),
    help="Change directory before running",
    metavar="DIR",
)
@click.option(
    "-l",
    "--log-level",
    type=LogLevel(),
    default="INFO",
    help="Set logging level",
    show_default=True,
)
@click.option(
    "-b",
    "--build-dir",
    type=click.Path(file_okay=False, dir_okay=True, writable=True, path_type=Path),
    default="build",
    help="Directory in which to create intermediate build artifacts",
    show_default=True,
    metavar="DIR",
)
@click.option(
    "-T",
    "--target-dir",
    type=click.Path(file_okay=False, dir_okay=True, writable=True, path_type=Path),
    default="target",
    help="Directory in which to create final assets",
    show_default=True,
    metavar="DIR",
)
@click.option(
    "--suite-dir",
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, readable=True, path_type=Path
    ),
    default="suite",
    help="Directory containing the definitions & templates for the test cases",
    show_default=True,
    metavar="DIR",
)
@click.pass_context
def main(
    ctx: click.Context,
    build_dir: Path,
    target_dir: Path,
    suite_dir: Path,
    chdir: Path | None,
    log_level: int,
) -> None:
    """
    Building test case repositories for versioningit.

    Visit <https://github.com/jwodder/versioningit-test-case-factory> for more
    information.
    """
    if chdir is not None:
        os.chdir(chdir)
    logging.basicConfig(
        format="%(asctime)s [%(levelname)-8s] %(message)s",
        datefmt="%H:%M:%S%z",
        level=log_level,
    )
    ctx.obj = CaseFactory(
        build_dir=build_dir, target_dir=target_dir, suite_dir=suite_dir
    )


@main.command()
@click.option("--clean", is_flag=True, help="Run `clean` before building")
@click.argument("id_globs", nargs=-1)
@click.pass_obj
def build(factory: CaseFactory, clean: bool, id_globs: tuple[str, ...]) -> None:
    """
    Build assets.

    If no arguments are given, all assets for all test cases are built.

    If any arguments are given, they are interpreted as glob patterns in which
    wildcards can match '/', and only the assets for the test cases whose IDs
    match one of the globs (along with their dependencies) are built.
    """
    if clean:
        factory.clean()
    factory.build(id_globs=id_globs)


@main.command()
@click.pass_obj
def clean(factory: CaseFactory) -> None:
    """Remove build and target directories"""
    factory.clean()


@main.command()
@click.option(
    "--no-purge",
    is_flag=True,
    help="Do not delete all assets already in the versioningit repository",
)
@click.argument(
    "versioningit-repo",
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, readable=True, path_type=Path
    ),
)
@click.pass_obj
def deploy(factory: CaseFactory, versioningit_repo: Path, no_purge: bool) -> None:
    """
    Deploy assets to versioningit.

    This command replaces the test case files in the given local clone of the
    versioningit repository with the contents of the target directory.
    """
    data_dir = versioningit_repo / "test" / "data"
    if not no_purge:
        for p in data_dir.glob("*.tar.gz"):
            log.debug("Removing %s", p)
            p.unlink()
        log.debug("Removing %s directory", data_dir / "repos")
        shutil.rmtree(data_dir / "repos")
    with iterpath(factory.target_dir, dirs=False, return_relative=True) as ip:
        for p in ip:
            src = factory.target_dir / p
            dest = data_dir / p
            dest.parent.mkdir(parents=True, exist_ok=True)
            log.debug("Moving %s to %s", src, dest)
            src.replace(dest)


@main.command()
@click.option(
    "--diff-dir",
    type=click.Path(file_okay=False, dir_okay=True, writable=True, path_type=Path),
    default="diffs",
    help="Directory in which to store diffs",
    show_default=True,
    metavar="DIR",
)
@click.argument(
    "versioningit-repo",
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, readable=True, path_type=Path
    ),
)
@click.pass_obj
def compare(factory: CaseFactory, diff_dir: Path, versioningit_repo: Path) -> None:
    """
    Diff archive assets against versioningit.

    This command compares the contents of the archive assets in the target
    directory against the archives currently present in the given local clone
    of the versioningit repository.  If a given archive asset differs from the
    one in versioningit, a diff of the contents is stored in `--diff-dir`.
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        comparer = Comparer(workdir=Path(tmpdir), diffdir=diff_dir)
        new_assets = dict(iter_archives(factory.target_dir))
        for key, p in iter_archives(versioningit_repo / "test" / "data"):
            if key not in new_assets:
                log.warning("Asset %s is in versioningit but not in target dir", key)
            else:
                comparer(key, p, new_assets.pop(key))
        for key in new_assets:
            log.warning("Asset %s is in target dir but not in versioningit", key)


def iter_archives(path: Path) -> Iterator[tuple[str, Path]]:
    selector = SelectGlob("*.tar.gz") | SelectGlob("*.zip")
    with iterpath(path, dirs=False, filter_files=selector, return_relative=True) as ip:
        for p in ip:
            if m := re.fullmatch(r"(?P<name>[^-]+)-[^-]+\.tar\.gz", p.name):
                key = p.parent / f"{m['name']}-*.tar.gz"
            else:
                key = p
            yield (key.as_posix(), path / p)


if __name__ == "__main__":
    main()
