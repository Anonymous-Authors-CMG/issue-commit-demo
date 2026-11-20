import pytest

from textkit import parse_duration, slugify, truncate, wrap


def test_slugify_basic():
    assert slugify("Hello, World!") == "hello-world"


def test_truncate_short_text_unchanged():
    assert truncate("short", 10) == "short"


def test_parse_duration_single_unit():
    assert parse_duration("45s") == 45
    assert parse_duration("2h") == 7200


def test_parse_duration_compound():
    assert parse_duration("1h30m") == 5400
    assert parse_duration("2m5s") == 125
    assert parse_duration("1h1m1s") == 3661


def test_parse_duration_rejects_garbage():
    with pytest.raises(ValueError):
        parse_duration("soon")


def test_wrap():
    assert wrap("the quick brown fox", width=10) == ["the quick", "brown fox"]
