from cv.resume import ResumeBank, EntrySection, TextSection, ListSection

def test_round_trip_keeps_all_sections(sample_bank):
    json_text = sample_bank.model_dump_json()
    loaded = ResumeBank.model_validate_json(json_text)

    assert loaded == sample_bank
    sections = [TextSection, EntrySection, ListSection]
    assert len(loaded.sections) == 3
    for position, section in enumerate(loaded.sections):
        assert isinstance(section, sections[position])