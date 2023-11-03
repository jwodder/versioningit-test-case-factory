from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
import inspect
import json
import logging
from pathlib import Path
from typing import Any, ClassVar, get_origin, get_type_hints
from in_place import InPlace
from .trees import Trees
from .vcs import Git, Mercurial

log = logging.getLogger()


@dataclass
class TestCase(ABC):
    ID: ClassVar[str | None] = None

    #: Basename of all test case artifacts (except for the sdist case, where
    #: it's a glob)
    NAME: ClassVar[str]

    #: Directory in $VERSIONINGIT_REPO/test/data where the artifacts will be
    #: stored
    PATH: ClassVar[Path]

    #: List of IDs of other test cases that must be created before this one
    DEPENDENCIES: ClassVar[list[str] | None] = None

    #: The directory in which all of the test case's assets are to be created.
    #: Guaranteed to exist upon instantiation.
    target_dir: Path

    #: A directory in which the test case should do all of its scratch work.
    #: Not guaranteed to exist upon instantiation.
    work_dir: Path

    #: For each dependency listed in `DEPENDENCIES`, this dict contains an
    #: entry with the dependency ID as the key and the completed test case as
    #: the value
    dependencies: dict[str, TestCase]

    trees: Trees

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        if not inspect.isabstract(cls):
            for name, ty in get_type_hints(cls, globalns=globals()).items():
                if get_origin(ty) is ClassVar and not hasattr(cls, name):
                    raise ValueError(f"ClassVar {name} not set on {cls.__name__}")

    @classmethod
    def get_id(cls) -> str:
        if cls.ID is not None:
            return cls.ID
        else:
            return (cls.PATH / cls.NAME).as_posix()

    def run(self) -> None:
        if self.needs_run():
            log.info("Building test case %s", self.get_id())
            self.build()
            self.check_assets()
        else:
            log.info("No need to build test case %s; skipping", self.get_id())

    @abstractmethod
    def needs_run(self) -> bool:
        ...

    @abstractmethod
    def build(self) -> None:
        ...

    @abstractmethod
    def check_assets(self) -> None:
        ...

    def mkwork(self) -> Path:
        # Returns self.work_dir for convenience
        self.work_dir.mkdir(parents=True, exist_ok=True)
        return self.work_dir

    def git(self) -> Git:
        return Git(path=self.work_dir, zipfile=self.target_dir / f"{self.NAME}.zip")

    def hg(self) -> Mercurial:
        return Mercurial(
            path=self.work_dir, zipfile=self.target_dir / f"{self.NAME}.zip"
        )

    def sync(self, tree: str) -> None:
        self.trees.sync_dir(self.mkwork(), tree)


class SdistCase(TestCase):
    def check_assets(self) -> None:
        assets = list(self.target_dir.glob(self.NAME))
        if not assets:
            raise RuntimeError(
                f"Test case {self.get_id()} failed to create any '{self.NAME}'"
                f" in {self.target_dir}"
            )
        if len(assets) > 1:
            raise RuntimeError(
                f"Test case {self.get_id()} created multiple '{self.NAME}' in"
                f" {self.target_dir}"
            )

    def needs_run(self) -> bool:
        return not any(self.target_dir.glob(self.NAME))


class ZipCase(TestCase):
    #: List of file extensions (including leading period) of assets that this
    #: test case will produce in addition to the primary zip (All assets have
    #: `NAME` as the basename)
    EXTRAS: ClassVar[list[str] | None] = None

    @property
    def zipfile(self) -> Path:
        return self.target_dir / f"{self.NAME}.zip"

    def needs_run(self) -> bool:
        return not self.zipfile.exists() or not all(
            self.asset_path(ext).exists() for ext in (self.EXTRAS or [])
        )

    def check_assets(self) -> None:
        if not self.zipfile.is_file():
            raise RuntimeError(
                f"Test case {self.get_id()} failed to create zipfile {self.zipfile}"
            )
        if self.EXTRAS:
            for ext in self.EXTRAS:
                extrafile = self.asset_path(ext)
                if not extrafile.is_file():
                    raise RuntimeError(
                        f"Test case {self.get_id()} failed to create extra file"
                        f" {extrafile}"
                    )
        for p in self.target_dir.glob(f"{self.NAME}.*"):
            ext = p.name.removeprefix(self.NAME)
            if ext != ".zip" and ext not in (self.EXTRAS or []):
                raise RuntimeError(
                    f"Test case {self.get_id()} created unexpected extra file {p}"
                )

    def asset_path(self, ext: str) -> Path:
        return self.target_dir / f"{self.NAME}{ext}"

    def json(self, data: Any, ext: str = ".json") -> None:
        with self.asset_path(ext).open("w", encoding="utf-8") as fp:
            json.dump(data, fp, indent=4)
            print(file=fp)

    def marks(self, *marks: str) -> None:
        self.asset_path(".marks").write_text(
            "".join(f"{m}\n" for m in marks), encoding="utf-8"
        )

    def dirty(self) -> None:
        """
        Make a tiny change to the workdir contents for the sake of creating a
        "dirty" repository
        """
        with InPlace(self.work_dir / "setup.cfg", encoding="utf-8") as fp:
            for line in fp:
                line = line.replace("test package", "dirty test package")
                fp.write(line)
