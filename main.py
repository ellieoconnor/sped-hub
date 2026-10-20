from datetime import date

import psycopg
from fastapi import FastAPI, HTTPException
from psycopg.rows import dict_row
from pydantic import BaseModel

app = FastAPI()


# Define the endpoint and return the dictionary
@app.get("/")
def read_root():
    return {"message": "hello"}

# STUDENT ENDPOINTS

# GET all students for a teacher
# TODO EO: Where will the teacher id come from? need dynamic teacher id
"""
TODO EO: When login exists, the server reads the logged-in teacher's id from their session cookie. It shouldn't come from the URL bc then anyone could type another number and see someone else's studnets. (answers the question: how do you stop one teacher from seeing another teacher's students?)
"""
# Current teacher id
CURRENT_TEACHER_ID = 2

@app.get("/students")
def list_students():
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        rows = conn.execute("SELECT * FROM students WHERE teacher_id = %s", (CURRENT_TEACHER_ID,)).fetchall()
    return rows

# One student (GET /students/{id}).
@app.get("/students/{student_id}")
def list_one_student(student_id: int):
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        row = conn.execute("SELECT * FROM students WHERE teacher_id= %s AND student_id=%s", (CURRENT_TEACHER_ID, student_id),).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Student not found")
    else:
        return row

# POST Add a student (POST /students). Done when you can add a student from the /docs page, then see it in step 2’s list. This is where you learn parameterized SQL and input validation.
class Student(BaseModel):
    first_name: str
    last_name: str
    grade_level: str
    birth_date: date
    accommodations: str
    last_iep_date: date | None = None
    next_iep_date: date | None = None

@app.post("/students")
def create_one_student(new_student: Student):
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        newRecord = conn.execute("INSERT INTO students (teacher_id, first_name, last_name, grade_level, birth_date, accommodations, last_iep_date, next_iep_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING *", (CURRENT_TEACHER_ID, new_student.first_name, new_student.last_name, new_student.grade_level, new_student.birth_date, new_student.accommodations, new_student.last_iep_date, new_student.next_iep_date),).fetchone()
    return newRecord

@app.delete("/students/{student_id}", status_code=204)
def delete_one_student(student_id: int):
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        record = conn.execute("DELETE FROM students WHERE student_id = %s AND teacher_id = %s RETURNING student_id", (student_id, CURRENT_TEACHER_ID),).fetchone()
    if not record:
        raise HTTPException(status_code=404, detail="Student not found")
    else:
        return

class StudentUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    grade_level: str | None = None
    birth_date: date | None = None
    accommodations: str | None = None
    last_iep_date: date | None = None
    next_iep_date: date | None = None

# TODO EO: refactor to update only the fields sent (option B), so a date can be cleared back to empty
@app.patch("/students/{student_id}")
def update_one_student(student_id: int, changes: StudentUpdate):
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        update_student = conn.execute("UPDATE students SET first_name = COALESCE(%s, first_name), last_name = COALESCE(%s, last_name), grade_level = COALESCE(%s, grade_level), birth_date = COALESCE(%s, birth_date), accommodations = COALESCE(%s, accommodations), last_iep_date = COALESCE(%s, last_iep_date), next_iep_date = COALESCE(%s, next_iep_date) WHERE student_id = %s AND teacher_id = %s RETURNING *", (changes.first_name, changes.last_name, changes.grade_level, changes.birth_date, changes.accommodations, changes.last_iep_date, changes.next_iep_date, student_id, CURRENT_TEACHER_ID), ).fetchone()
        if not update_student:
            raise HTTPException(status_code=404, detail="Student not found.")
        else:
            return update_student



#TEACHER ENDPOINTS

# GET all teachers
@app.get("/teachers")
def list_teachers():
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        rows = conn.execute("SELECT first_name, last_name FROM teachers").fetchall()
    return rows