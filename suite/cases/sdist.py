from __future__ import annotations
from pathlib import Path
from build import ProjectBuilder
from build.env import DefaultIsolatedEnv
from factory.case import SdistCase


class TestCase(SdistCase):
    NAME = "mypackage-*.tar.gz"
    PATH = Path()
    DEPENDENCIES = ["onbuild-write"]

    def build(self) -> None:
        repopath = self.dependencies["onbuild-write"].work_dir
        with DefaultIsolatedEnv() as env:
            builder = ProjectBuilder.from_isolated_env(env, repopath)
            env.install(builder.build_system_requires)
            env.install(builder.get_requires_for_build("sdist"))
            builder.build("sdist", self.target_dir)
