from setuptools import setup


def my_tag2version(tag, params):  # noqa: U100
    if tag.startswith("rel_"):
        tag = tag[4:]
    return tag.replace("_", ".")


if __name__ == "__main__":
    setup()
