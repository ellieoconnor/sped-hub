import psycopg
from fastapi import APIRouter, HTTPException
from psycopg.rows import dict_row

from config import CURRENT_TEACHER_ID
from models import StudentCreate, StudentUpdate

router = APIRouter(prefix="/students", tags=["students"])

# GET all students for a teacher
# TODO EO: Where will the teacher id come from? need dynamic teacher id; When login exists, the server reads the logged-in teacher's id from their session cookie. It shouldn't come from the URL bc then anyone could type another number and see someone else's students. (answers the question: how do you stop one teacher from seeing another teacher's students?)

@router.get("")
def list_students():
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        students = conn.execute("SELECT * FROM students WHERE teacher_id = %s", (CURRENT_TEACHER_ID,)).fetchall()
    return students

# One student (GET /students/{id}).
@router.get("/{student_id}")
def get_student(student_id: int):
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        student = conn.execute("SELECT * FROM students WHERE teacher_id= %s AND student_id=%s", (CURRENT_TEACHER_ID, student_id),).fetchone()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    return student

# POST Add a student (POST /students)
@router.post("")
def create_student(new_student: StudentCreate):
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        student = conn.execute(
            """
            INSERT INTO students (
                teacher_id, 
                first_name, 
                last_name, 
                grade_level, 
                birth_date, 
                accommodations, 
                last_iep_date, 
                next_iep_date
            ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) 
            RETURNING *
            """,
            (
                CURRENT_TEACHER_ID, 
                new_student.first_name, 
                new_student.last_name, 
                new_student.grade_level, 
                new_student.birth_date, 
                new_student.accommodations, 
                new_student.last_iep_date, 
                new_student.next_iep_date
            ),
            ).fetchone()
    return student

# DELETE one student
@router.delete("/{student_id}", status_code=204)
def delete_student(student_id: int):
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        student = conn.execute("DELETE FROM students WHERE student_id = %s AND teacher_id = %s RETURNING student_id", (student_id, CURRENT_TEACHER_ID),).fetchone()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

# PATCH to update one student
# TODO EO: refactor to update only the fields sent (option B), so a date can be cleared back to empty
@router.patch("/{student_id}")
def update_student(student_id: int, changes: StudentUpdate):
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        student = conn.execute(
            """
            UPDATE students 
            SET 
                first_name = COALESCE(%s, first_name), 
                last_name = COALESCE(%s, last_name), 
                grade_level = COALESCE(%s, grade_level), 
                birth_date = COALESCE(%s, birth_date), 
                accommodations = COALESCE(%s, accommodations), 
                last_iep_date = COALESCE(%s, last_iep_date), 
                next_iep_date = COALESCE(%s, next_iep_date) 
            WHERE student_id = %s AND teacher_id = %s RETURNING *
            """, 
            (
                changes.first_name, 
                changes.last_name, 
                changes.grade_level, 
                changes.birth_date, 
                changes.accommodations, 
                changes.last_iep_date, 
                changes.next_iep_date, 
                student_id, 
                CURRENT_TEACHER_ID
            ),
            ).fetchone()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student