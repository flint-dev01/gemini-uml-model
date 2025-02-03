from pydantic import BaseModel

class UsecaseCreate(BaseModel):
    srs_text: str

class UmlResponse(UsecaseCreate):
    image: str

class SequenceCreate(BaseModel):
    srs_text: str
    use_cases: list
    usecase_code: str
    
class ActivityCreate(BaseModel):
    srs_text: str
    actors: list
    usecase_code: str
