from __future__ import annotations
from collections.abc import Iterator
import logging
import os
from pathlib import Path
import re
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
    help="Directory in which to create final artifacts",
    show_default=True,
    metavar="DIR",
)
@click.option(
    "--case-dir",
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, readable=True, path_type=Path
    ),
    default="cases",
    help="Directory containing test case definitions",
    show_default=True,
    metavar="DIR",
)
@click.option(
    "--tree-dir",
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, readable=True, path_type=Path
    ),
    default="trees",
    help="Directory containing file trees for use in building test cases",
    show_default=True,
    metavar="DIR",
)
@click.option(
    "--patchdef-dir",
    type=click.Path(
        exists=True, file_okay=False, dir_okay=True, readable=True, path_type=Path
    ),
    default="patchdefs",
    help="Directory containing definitions for patches used in building test cases",
    show_default=True,
    metavar="DIR",
)
@click.pass_context
def main(
    ctx: click.Context,
    build_dir: Path,
    target_dir: Path,
    case_dir: Path,
    tree_dir: Path,
    patchdef_dir: Path,
    chdir: Path | None,
    log_level: int,
) -> None:
    if chdir is not None:
        os.chdir(chdir)
    logging.basicConfig(
        format="%(asctime)s [%(levelname)-8s] %(message)s",
        datefmt="%H:%M:%S%z",
        level=log_level,
    )
    ctx.obj = CaseFactory(
        build_dir=build_dir,
        target_dir=target_dir,
        case_dir=case_dir,
        tree_dir=tree_dir,
        patchdef_dir=patchdef_dir,
    )


@main.command()
@click.pass_obj
def build(factory: CaseFactory) -> None:
    factory.build()


@main.command()
@click.pass_obj
def clean(factory: CaseFactory) -> None:
    factory.clean()


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
