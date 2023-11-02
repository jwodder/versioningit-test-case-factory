def my_tag2version(tag, params):  # noqa: U100
    if tag.startswith("rel_"):
        tag = tag[4:]
    return tag.replace("_", ".")
