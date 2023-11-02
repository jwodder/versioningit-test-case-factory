from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from graphlib import TopologicalSorter
import json
import logging
from pathlib import Path
import shutil
import sys
from typing import Any
from .case import TestCase
from .trees import PatchDef, Trees

log = logging.getLogger()


@dataclass
class CaseFactory:
    build_dir: Path
    target_dir: Path
    case_dir: Path
    tree_dir: Path
    patchdef_dir: Path

    def build(self) -> None:
        self.build_dir.mkdir(parent=True, exist_ok=True)
        self.target_dir.mkdir(parent=True, exist_ok=True)
        patchdefs = self.gather_patchdefs()
        trees = Trees(
            tree_dir=self.tree_dir,
            patch_dir=self.build_dir / "patches",
            patchdefs=patchdefs,
        )
        cases = self.gather_cases()
        depmap: dict[str, list[str]] = defaultdict(list)
        for c in cases:
            cname = c.get_id()
            for dep in c.DEPENDENCIES or []:
                if dep not in cases:
                    raise RuntimeError(
                        f"Test case {cname} depends on unknown test case {dep}"
                    )
                depmap[cname].append(dep)
        sorter = TopologicalSorter(depmap)
        completed: dict[str, TestCase]
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
                if work_dir.exist():
                    crash_dir = self.build_dir / "crash"
                    crash_dir.mkdir(parents=True, exist_ok=True)
                    now = datetime.now(timezone.utc)
                    name = cid.replace("/", "--") + "-" + now.strftime("%Y%m%dT%H%M%S")
                    work_dir.rename(crash_dir / name)
                    log.info("Test case work directory saved at %s", crash_dir / name)
                sys.exit(1)

    def clean(self) -> None:
        shutil.rmtree(self.build_dir)
        shutil.rmtree(self.target_dir)

    def gather_patchdefs(self) -> dict[str, PatchDef]:
        patchdefs = {}
        for p in self.patchdef_dir.glob("*.json"):
            with p.open(encoding="utf-8") as fp:
                pdef = PatchDef.model_validate(json.load(fp))
                patchdefs[p.stem] = pdef
        return patchdefs

    def gather_cases(self) -> list[type[TestCase]]:
        cases = {}
        for p in self.case_dir.rglob("*.py"):
            context: dict[str, Any] = {}
            exec(p.read_text(encoding="utf-8"), globals=context)
            found = False
            for val in context.values():
                if issubclass(val, TestCase):
                    found = True
                    cid = val.get_id()
                    if cid in cases:
                        raise RuntimeError(f"Multiple test cases found with id {cid!r}")
                    else:
                        cases[cid] = val
            if not found:
                raise RuntimeError(f"No test cases found in case file {p}")
        return cases
