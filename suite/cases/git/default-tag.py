from __future__ import annotations
from pathlib import Path
from factory.case import ZipCase


class TestCase(ZipCase):
    """
    Produces a Git repository without any tags but with ``vcs.default-tag`` set
    """

    NAME = "default-tag"
    PATH = Path("repos", "git")
    EXTRAS = [".json", ".fields.json"]

    def build(self) -> None:
        git = self.git()
        self.sync("0100-code")
        git.commit("Some code")
        self.sync("0200-packaged")
        git.commit("Packaging")
        self.sync("0300-default-tag")
        git.commit("Set default-tag")
        git.zip()
        info = git.get_info()
        self.json(
            {
                "version": f"0.0.0.post2+g{info.rev}",
                "next_version": "0.1.0",
                "logmsgs": [
                    {
                        "level": "INFO",
                        "message": "`git describe --long --dirty --always --tags` returned a hash instead of a tag; falling back to default tag 'v0.0.0'",
                    }
                ],
            }
        )
        info.save(self.asset_path(".fields.json"))
