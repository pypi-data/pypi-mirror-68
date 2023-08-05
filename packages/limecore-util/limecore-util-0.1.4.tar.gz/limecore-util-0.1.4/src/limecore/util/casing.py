import re


def to_snakecase(s: str, separator: str = "_"):
    return separator.join(x.lower() for x in re.findall("[A-Z]+[^A-Z]*", s))
