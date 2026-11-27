import pytest
from pydantic import ValidationError

from cv.resume import BulletPoint, Entry, Origin, TextItem, YearMonth


def test_text_item_rejects_empty_text():
    with pytest.raises(ValidationError):
        TextItem(text="")


def test_rephrased_item_requires_source_id():
    with pytest.raises(ValidationError):
        TextItem(text="Monitored 200+ devices", origin=Origin.REPHRASED)


def test_bullet_point_requires_a_variant():
    with pytest.raises(ValidationError):
        BulletPoint(variants=[])


def test_entry_rejects_end_before_start():
    with pytest.raises(ValidationError):
        Entry(start=YearMonth(year=2025), end=YearMonth(year=2020))


def test_entry_rejects_end_and_ongoing_together():
    with pytest.raises(ValidationError):
        Entry(start=YearMonth(year=2024), end=YearMonth(year=2025), ongoing=True)


def test_entry_allows_start_only():
    entry = Entry(start=YearMonth(year=2024, month=3))
    assert entry.end is None