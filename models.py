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

class GoalCreate(BaseModel):
    category_id: int
    goal_text: str
    baseline_value: float | None = None
    baseline_notes: str | None = None
    target_value: float | None = None
    target_notes: str | None = None
    start_date: date | None = None
    due_date: date

class GoalUpdate(BaseModel):
    category_id: int | None = None
    goal_text: str | None = None
    baseline_value: float | None = None
    baseline_notes: str | None = None
    target_value: float | None = None
    target_notes: str | None = None
    start_date: date | None = None
    due_date: date | None = None