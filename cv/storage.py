from cv.profiles import TargetProfiles

from cv.resume import ResumeBank
from pathlib import Path
from pydantic import BaseModel
from typing import TypeVar

T = TypeVar('T', bound = BaseModel)

FILE_NAMES: dict[type[BaseModel], str] = {
    ResumeBank: 'resume_bank.json',
    TargetProfiles: 'target_profiles.json'
}

def file_for(model_type: type[BaseModel], folder: Path):
    try:
        return folder / FILE_NAMES[model_type]
    except KeyError:
        raise TypeError(f"{model_type.__name__} is not supported by storage")

def save_to_json(obj: BaseModel, folder: Path):
    folder.mkdir(parents = True, exist_ok = True)
    file = file_for(type(obj), folder)
    tmp = file.with_name(file.name + ".temp")
    tmp.write_text(obj.model_dump_json(indent = 2), encoding = 'utf-8')
    tmp.replace(file)

def load_from_json(model_type: type[T], folder: Path):
    file = file_for(model_type, folder)
    if not file.exists():
        return None
    return model_type.model_validate_json(file.read_text(encoding = 'utf-8'))
