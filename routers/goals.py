import psycopg
from fastapi import APIRouter, HTTPException
from psycopg.rows import dict_row

from config import CURRENT_TEACHER_ID

router = APIRouter(tags=["goals"])

# GET one student's goals
@router.get("students/{student_id}/goals")
def list_student_goals(student_id: int):
    # check the student belongs to the current teacher
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        student = conn.execute("SELECT * FROM students WHERE teacher_id = %s AND student_id = %s", (CURRENT_TEACHER_ID, student_id),).fetchone()

        goals = conn.execute("SELECT * FROM student_goals WHERE student_id = %s", (student_id,)).fetchall()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return goals