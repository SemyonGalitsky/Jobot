import pytest
from pydantic import ValidationError

from cv.profiles import SectionRule, TargetProfile


def test_rule_rejects_id_both_pinned_and_excluded():
    with pytest.raises(ValidationError):
        SectionRule(section_id="s1", pinned_ids=["a"], excluded_ids=["a"])


def test_profile_rejects_two_rules_for_same_section():
    with pytest.raises(ValidationError):
        TargetProfile(
            name="Test",
            section_rules=[SectionRule(section_id="s1"), SectionRule(section_id="s1")],
        )


def test_profile_rejects_page_limit_zero():
    with pytest.raises(ValidationError):
        TargetProfile(name="Test", page_limit=0)