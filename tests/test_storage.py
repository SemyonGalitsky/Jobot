import pytest

from cv.profiles import TargetProfiles
from cv.resume import ResumeBank
from cv.storage import load_from_json, save_to_json


def test_round_trip_save_and_load_bank(sample_bank, tmp_path):
    save_to_json(sample_bank, tmp_path)
    loaded = load_from_json(ResumeBank, tmp_path)
    assert loaded == sample_bank, "saved and/or loaded incorrectly"

def test_round_trip_save_and_load_profiles(sample_profiles, tmp_path):
    save_to_json(sample_profiles, tmp_path)
    loaded = load_from_json(TargetProfiles, tmp_path)
    assert loaded == sample_profiles, "saved and/or loaded incorrectly"
    

def test_load_bank_missing_file_returns_none(tmp_path):
    loaded = load_from_json(ResumeBank, tmp_path)
    assert loaded is None

def test_load_profiles_missing_file_returns_none(tmp_path):
    loaded = load_from_json(TargetProfiles, tmp_path)
    assert loaded is None

def test_save_unsupported_type_raises(sample_header, tmp_path):
    with pytest.raises(TypeError):
        save_to_json(sample_header, tmp_path)

