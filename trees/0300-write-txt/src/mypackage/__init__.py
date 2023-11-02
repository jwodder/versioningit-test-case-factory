""" A test package """

from pathlib import Path

__version__ = Path(__file__).with_name("version.txt").read_text().strip()
__author__ = "John Thorvald Wodder II"
__author_email__ = "mypackage@varonathe.org"
__license__ = "MIT"
