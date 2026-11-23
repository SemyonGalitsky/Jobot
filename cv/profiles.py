from pydantic import BaseModel, Field, model_validator
from enum import StrEnum
from cv.id_generator import IdGenerator


class ContentMode(StrEnum):
    SELECT      = 'select'
    REPHRASE    = 'rephrase'
    GENERATE    = 'generate'

class SectionState(StrEnum):
    ALWAYS      = 'always'
    AUTO        = 'auto'
    NEVER       = 'never'

class SectionRule(BaseModel):
    section_id:     str
    include:        SectionState    = SectionState.AUTO
    order:          int | None      = Field(default = None, ge = 1) #none means ai decides
    mode:           ContentMode     = ContentMode.SELECT
    max_items:      int | None      = Field(default = None, ge = 1)
    max_bullets:    int | None      = Field(default = None, ge = 1)
    pinned_ids:     list[str]       = []
    excluded_ids:   list[str]       = []

    @model_validator(mode="after")
    def validate_section_rule(self):
        overlap = set(self.excluded_ids) & set(self.pinned_ids)
        if overlap:
            raise ValueError(f"IDs both pinned and excluded: {sorted(overlap)}")
        return self

class TargetProfile(BaseModel):
    id:             str                 = Field(default_factory=IdGenerator.generate_id)
    name:           str
    headline_mode:  ContentMode         = ContentMode.SELECT
    keywords:       list[str]           = []
    section_rules:  list[SectionRule]   = []
    page_limit:     int                 = Field(default = 1, ge = 1)

    @model_validator(mode="after")
    def validate_target_profiles(self):
        seen = set()
        for section_rule in self.section_rules:
            if section_rule.section_id in seen:
                raise ValueError("the same section cant have 2 rules")
            seen.add(section_rule.section_id)
        return self

class TargetProfiles(BaseModel):
    profiles:    list[TargetProfile] = []