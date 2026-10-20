from datetime import date

from pydantic import BaseModel


class StudentCreate(BaseModel):
    first_name: str
    last_name: str
    grade_level: str
    birth_date: date
    accommodations: str
    last_iep_date: date | None = None
    next_iep_date: date | None = None

class StudentUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    grade_level: str | None = None
    birth_date: date | None = None
    accommodations: str | None = None
    last_iep_date: date | None = None
    next_iep_date: date | None = None