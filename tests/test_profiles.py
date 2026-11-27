
def test_round_trip_profiles(sample_profiles):
    json_text = sample_profiles.model_dump_json()
    loaded = sample_profiles.model_validate_json(json_text)

    assert loaded == sample_profiles