import re
import unicodedata


def slugify(text, sep="-"):
    """Turn a title into a URL slug: "Hello, World" -> "hello-world"."""
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", sep, text)
    return text.strip(sep)


def truncate(text, width, ellipsis="..."):
    """Shorten text to at most `width` characters, marking the cut."""
    if len(text) <= width:
        return text
    if width <= len(ellipsis):
        return ellipsis[:width]
    return text[:width - len(ellipsis)] + ellipsis


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
    lines, current = [], ""
    for word in text.split():
        if current and len(current) + 1 + len(word) > width:
            lines.append(current)
            current = word
        else:
            current = "%s %s" % (current, word) if current else word
    if current:
        lines.append(current)
    return lines
