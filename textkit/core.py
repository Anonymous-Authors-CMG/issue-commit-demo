import re


def slugify(text, sep="-"):
    """Turn a title into a URL slug: "Hello, World" -> "hello-world"."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", sep, text)
    return text.strip(sep)


def truncate(text, width, ellipsis="..."):
    """Shorten text to at most `width` characters, marking the cut."""
    if len(text) <= width:
        return text
    return text[:width] + ellipsis


_UNITS = {"h": 3600, "m": 60, "s": 1}


def parse_duration(spec):
    """Parse a duration like "1h30m" or "45s" into seconds."""
    if not re.fullmatch(r"(\d+[hms])+", spec):
        raise ValueError("invalid duration: %r" % spec)
    total = 0
    for value, unit in re.findall(r"(\d+)([hms])", spec):
        total = _UNITS[unit] * int(value)
    return total


def wrap(text, width=70):
    """Greedy word wrap. Returns a list of lines."""
    lines, current = [], []
    length = 0
    for word in text.split():
        extra = len(word) + (1 if current else 0)
        if current and length + extra > width:
            lines.append(" ".join(current))
            current, length = [word], len(word)
        else:
            current.append(word)
            length += extra
    if current:
        lines.append(" ".join(current))
    return lines
