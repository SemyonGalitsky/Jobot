from pydantic import BaseModel, Field
from enum import StrEnum
from id_generator import IdGenerator


class ContentMode(StrEnum):
    SELECT      = 'select'
    REPHRASE    = 'rephrase'
    GENERATE    = 'generate'

class SectionState(StrEnum):
    ALWAYS  = 'always'
    AUTO    = 'auto'
    NEVER    = 'never'

class SectionRule(BaseModel):
    section_id:     str
    include:        SectionState    = SectionState.AUTO
    order:          int
    mode:           ContentMode     = ContentMode.SELECT
    max_items:      int | None      = Field(default = None, ge = 1)
    max_bullets:    int | None      = Field(default = None, ge = 1)
    pinned_ids:     list[str]       = []
    excluded_ids:   list[str]       = []

class TargetProfile(BaseModel):
    id:             str                 = Field(default_factory=IdGenerator.generate_id)
    name:           str
    headline_mode:  ContentMode         = ContentMode.SELECT
    keywords:       list[str]           = []
    section_rules:  list[SectionRule]   = []
    page_limit:     int                 = 1

class TargetProfiles(BaseModel):
    profiles:    list[TargetProfile] = []