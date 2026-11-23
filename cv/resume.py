from pydantic import BaseModel, Field, model_validator
from typing import Literal, Annotated
from enum import StrEnum
from cv.id_generator import IdGenerator

class SectionKind(StrEnum):
    SUMMARY             = 'summary'
    WORK                = 'work'
    MILITARY            = 'military'
    EDUCATION           = 'education'
    PROJECTS            = 'projects'
    VOLUNTEER           = 'volunteer'
    EXTRACURRICULAR     = 'extracurricular'
    CERTIFICATIONS      = 'certifications'
    AWARDS              = 'awards'
    PUBLICATIONS        = 'publications'
    TALKS               = 'talks'
    MEMBERSHIPS         = 'memberships'
    PATENTS             = 'patents'
    SKILLS              = 'skills'
    LANGUAGES           = 'languages'
    INTERESTS           = 'interests'
    REFERENCES          = 'references'
    CUSTOM              = 'custom'

class EmploymentType(StrEnum):
    FULL_TIME           = 'full time'
    PART_TIME           = 'part time'
    CONTRACT            = 'contract'
    FREELANCE           = 'freelance'
    INTERNSHIP          = 'internship'

class Origin(StrEnum):
    USER                = 'user'
    REPHRASED           = 'rephrased'
    GENERATED           = 'generated'

class TextItem(BaseModel): #used for headlines, job titles, summaries, bullets and skills
    id:                 str                     = Field(default_factory=IdGenerator.generate_id)
    text:               str                     = Field(min_length = 1)
    tags:               list[str]               = []
    origin:             Origin                  = Origin.USER
    source_id:          str | None              = None

    @model_validator(mode="after")
    def validate_text_item(self):
        if bool(self.origin == Origin.REPHRASED) != bool(self.source_id):
            raise ValueError("rephrased must be paired with a source id")
        return self

class YearMonth(BaseModel):
    year:               int                     = Field(ge=1900)
    month:              int | None              = Field(default=None, ge=1, le=12)

class ItemGroup(BaseModel):
    id:                 str                     = Field(default_factory=IdGenerator.generate_id)
    title:              str
    items:              list[TextItem]          = []
    description:        str | None              = None

class BulletPoint(BaseModel):
    id:                 str                     = Field(default_factory=IdGenerator.generate_id)
    variants:           list[TextItem]          = Field(min_length = 1)


class Entry(BaseModel):
    id:                 str                     = Field(default_factory=IdGenerator.generate_id)
    titles:             list[TextItem]          = []
    organization:       str | None              = None
    subtitle:           str | None              = None
    location:           str | None              = None
    url:                str | None              = None
    start:              YearMonth | None        = None
    end:                YearMonth | None        = None
    ongoing:            bool                    = False
    employment_type:    EmploymentType | None   = None
    scope:              str | None              = None
    description:        str | None              = None
    bullets:            list[BulletPoint]       = []
    tool_ids:           list[str]               = []

    @model_validator(mode="after")
    def validate_entry(self):
        if bool(self.start) < bool(self.end) + bool(self.ongoing):
            raise ValueError("End or ongoing requires start, and they cannot be combined")
        if self.end and self.start:
            if self.start.year > self.end.year:
                raise ValueError("Impossible dates")
            if bool(self.start.month) != bool(self.end.month):
                raise ValueError("Months are set for either or neither dates")
            if self.start.month and self.end.month:
                if (self.start.year == self.end.year) and (self.start.month > self.end.month):
                    raise ValueError("Impossible dates")
        return self

class Section(BaseModel):
    id:                 str                     = Field(default_factory=IdGenerator.generate_id)
    kind:               SectionKind
    title:              str

class TextSection(Section):
    shape:              Literal["text"]         = "text"
    variants:           list[TextItem]          = []

class EntrySection(Section):
    shape:              Literal["entry"]        = "entry"
    entries:            list[Entry]             = []

class ListSection(Section):
    shape:              Literal["list"]         = "list"
    groups:             list[ItemGroup]         = []

class Header(BaseModel):
    full_name:          str
    headlines:          list[TextItem]          = []
    email:              str | None              = None
    phone:              str | None              = None
    location:           str | None              = None
    linkedin:           str | None              = None
    github:             str | None              = None
    website:            str | None              = None
    photo_path:         str | None              = None

    @model_validator(mode="after")
    def validate_header(self):
        if not self.email and not self.phone:
            raise ValueError("Either email or phone must be provided")
        return self

AnySection = Annotated[
    TextSection | EntrySection | ListSection,
    Field(discriminator = "shape")
]

class ResumeBank(BaseModel):
    header:     Header
    sections:    list[AnySection]   = []
    about_me:   str                 | None = None
