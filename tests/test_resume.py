from cv.resume import ResumeBank, Header, EntrySection, Entry, TextItem, SectionKind

def testRoundTripKeepsAllSections():
    bank = ResumeBank(
        header=Header(full_name="Test User", email="test@example.com"),
        sections=[
            EntrySection(
                kind=SectionKind.WORK,
                title="Experience",
                entries=[Entry(titles=[TextItem(text="NOC Technician")],
                               bullets=[TextItem(text="Monitored network devices")])],
            ),
            
        ],
    )

    json_text = bank.model_dump_json()
    loaded = ResumeBank.model_validate_json(json_text)

    assert loaded == bank
    assert isinstance(loaded.sections[0], EntrySection)