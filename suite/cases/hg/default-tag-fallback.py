from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    """
    Produces a Mercurial repository in which versioningit is configured to
    exclude all tags, leading to falling back to ``vcs.default-tag``.
    """

    ID = "hg-default-tag-fallback"
    NAME = "default-tag-fallback"
    PATH = Path("repos", "hg")
    EXTRAS = [".json", ".fields.json"]

    def build(self) -> None:
        hg = self.hg()
        self.sync("0200-hg-packaged")
        hg.commit("Packaging")
        hg.tag("0.1.0")
        self.sync("0300-hg-default-tag")
        with (self.work_dir / "pyproject.toml").open("a", encoding="utf-8") as fp:
            print("pattern = 're:^v'", file=fp)
        hg.commit("Set default-tag and pattern")
        hg.tag("0.2.0")
        hg.zip()
        info = hg.get_info(pattern="rev:^v")
        self.json(
            {
                "version": f"0.0.0.post3+h{info.rev}",
                "next_version": "0.1.0",
                "logmsgs": [
                    {
                        "level": "INFO",
                        "message": "No latest tag (pattern = 're:^v'); falling back to default tag 'v0.0.0'",
                    }
                ],
            },
        )
        info.save(self.asset_path(".fields.json"))
