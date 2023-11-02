""" A test package """

try:
    from importlib.metadata import version
except ImportError:
    from importlib_metadata import version

__version__ = version("mypackage")
__author__ = "John Thorvald Wodder II"
__author_email__ = "mypackage@varonathe.org"
__license__ = "MIT"
