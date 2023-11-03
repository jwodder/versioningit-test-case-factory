from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone
from graphlib import TopologicalSorter
import inspect
import logging
from pathlib import Path
import shutil
import sys
from typing import Any
from .case import TestCase
from .trees import Trees

log = logging.getLogger()


@dataclass
class CaseFactory:
    build_dir: Path
    target_dir: Path
    suite_dir: Path

    def __post_init__(self) -> None:
        self.build_dir = self.build_dir.absolute()
        self.target_dir = self.target_dir.absolute()
        self.suite_dir = self.suite_dir.absolute()

    @property
    def case_dir(self) -> Path:
        return self.suite_dir / "cases"

    @property
    def tree_dir(self) -> Path:
        return self.suite_dir / "trees"

    def build(self) -> None:
        self.build_dir.mkdir(parents=True, exist_ok=True)
        self.target_dir.mkdir(parents=True, exist_ok=True)
        trees = Trees(tree_dir=self.tree_dir)
        cases = self.gather_cases()
        depmap: dict[str, list[str]] = {}
        for c in cases.values():
            cname = c.get_id()
            depmap[cname] = []
            for dep in c.DEPENDENCIES or []:
                if dep not in cases:
                    raise RuntimeError(
                        f"Test case {cname} depends on unknown test case {dep}"
                    )
                depmap[cname].append(dep)
        sorter = TopologicalSorter(depmap)
        completed: dict[str, TestCase] = {}
        for cid in sorter.static_order():
            c = cases[cid]
            target = self.target_dir / c.PATH
            target.mkdir(parents=True, exist_ok=True)
            work_dir = self.build_dir / "work" / cid
            dependencies = {dep: completed[dep] for dep in (c.DEPENDENCIES or [])}
            cobj = c(
                target_dir=target,
                work_dir=work_dir,
                dependencies=dependencies,
                trees=trees,
            )
            try:
                cobj.run()
            except Exception:
                log.exception("Test case %s failed", cid)
                if work_dir.exists():
                    crash_dir = self.build_dir / "crash"
                    crash_dir.mkdir(parents=True, exist_ok=True)
                    now = datetime.now(timezone.utc)
                    name = cid.replace("/", "--") + "-" + now.strftime("%Y%m%dT%H%M%S")
                    work_dir.rename(crash_dir / name)
                    log.info("Test case work directory saved at %s", crash_dir / name)
                sys.exit(1)
            completed[cid] = cobj

    def clean(self) -> None:
        log.info("Removing %s ...", self.build_dir)
        shutil.rmtree(self.build_dir)
        log.info("Removing %s ...", self.target_dir)
        shutil.rmtree(self.target_dir)

    def gather_cases(self) -> dict[str, type[TestCase]]:
        cases = {}
        path_names = set()
        for p in self.case_dir.rglob("*.py"):
            log.debug("Loading cases from %s ...", p)
            context: dict[str, Any] = {}
            exec(p.read_text(encoding="utf-8"), context)
            found = False
            for val in context.values():
                if (
                    inspect.isclass(val)
                    and not inspect.isabstract(val)
                    and issubclass(val, TestCase)
                ):
                    found = True
                    cid = val.get_id()
                    if cid in cases:
                        raise RuntimeError(f"Multiple test cases found with id {cid!r}")
                    else:
                        if (p := val.PATH / val.NAME) in path_names:
                            raise RuntimeError(
                                f"Multiple test cases with PATH={val.PATH} and"
                                f" NAME={val.NAME!r}"
                            )
                        path_names.add(p)
                        cases[cid] = val
            if not found:
                raise RuntimeError(f"No test cases found in case file {p}")
        return cases
