from cv.resume import ResumeBank, Header, EntrySection, Entry, TextItem, SectionKind, TextSection, ListSection, ItemGroup
from cv.profiles import TargetProfiles, TargetProfile, SectionRule, ContentMode, SectionState
import pytest
@pytest.fixture
def sample_bank():
    return ResumeBank(
            header = Header(full_name = "Test User", email = "test@example.com"),
        sections = [
            TextSection(
                kind = SectionKind.SUMMARY,
                title = "Summary",
                variants = [
                    TextItem(text="Software engineer with experience in networking and backend systems."),
                    TextItem(text="Cybersecurity-focused developer skilled in Python and network monitoring.", tags=["security"]),

                ]
            ),
            EntrySection(
                kind = SectionKind.WORK,
                title = "Experience",
                entries = [
                    Entry(
                        titles=[TextItem(text = "NOC Technician")],
                        bullets=[TextItem(text = "Monitored network devices"),
                                 TextItem(text = "Maintained Secuirty across 12 different facilities")
                                 ],
                    )
                ]
            ),
            ListSection(
                kind = SectionKind.SKILLS,
                title = "Skills",
                groups = [
                    ItemGroup(
                        title = "Languages",
                        items = [
                            TextItem(text = "Python"),
                            TextItem(text = "Java"),
                        ]
                    ),
                    ItemGroup(
                        title = "Tools",
                        items = [
                            TextItem(text = "Docker"),
                            TextItem(text = "Wireshark"),
                        ]
                    )
                ]
            )
        ]
    )

@pytest.fixture
def sample_header():
    return Header(full_name = "Test User 2", email = "test2@example.com")

@pytest.fixture
def sample_profiles(sample_bank):
    summary, work, skills = sample_bank.sections
    wireshark = skills.groups[1].items[1]
    return TargetProfiles(
        profiles=[
            TargetProfile(
                name="NOC student",
                headline_mode=ContentMode.REPHRASE,
                keywords=["NOC", "monitoring", "סטודנט", "משמרות"],
                section_rules=[
                    SectionRule(section_id=summary.id, include=SectionState.ALWAYS,
                                order=1, mode=ContentMode.GENERATE, max_items=1),
                    SectionRule(section_id=work.id, include=SectionState.ALWAYS,
                                order=2, mode=ContentMode.REPHRASE, max_items=4, max_bullets=3),
                    SectionRule(section_id=skills.id, include=SectionState.ALWAYS,
                                order=3, pinned_ids=[wireshark.id]),
                ],
            ),
            TargetProfile(
                name="SOC analyst student",
                keywords=["SOC", "SIEM", "security"],
                section_rules=[
                    SectionRule(section_id="sec-summary", include=SectionState.AUTO,
                                order=1, mode=ContentMode.SELECT),
                    SectionRule(section_id="sec-work", include=SectionState.ALWAYS,
                                order=2, mode=ContentMode.REPHRASE,
                                excluded_ids=["item-docker"]),
                ],
            ),
            TargetProfile(
                name="Backend student",
                headline_mode=ContentMode.GENERATE,
                page_limit=2,
                section_rules=[
                    SectionRule(section_id="sec-skills", include=SectionState.ALWAYS,
                                order=1, pinned_ids=["item-python", "item-docker"]),
                    SectionRule(section_id="sec-work", include=SectionState.NEVER,
                                order=2),
                ],
            ),
        ]
    )