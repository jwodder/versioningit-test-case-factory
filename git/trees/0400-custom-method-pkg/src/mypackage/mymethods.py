def my_tag2version(tag, params):
    if tag.startswith("rel_"):
        tag = tag[4:]
    return tag.replace("_", ".")
