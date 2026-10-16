import psycopg
from fastapi import FastAPI, HTTPException
from psycopg.rows import dict_row

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

# One student (GET /students/{id}). Done when a real id returns that student and a made-up id returns a 404 instead of crashing.
@app.get("/students/{student_id}")
def list_one_student(student_id: int):
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        row = conn.execute("SELECT * FROM students WHERE teacher_id= %s AND student_id=%s", (CURRENT_TEACHER_ID, student_id),).fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Student not found")
    else:
        return row


#TEACHER ENDPOINTS

# GET all teachers
@app.get("/teachers")
def list_teachers():
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        rows = conn.execute("SELECT first_name, last_name FROM teachers").fetchall()
    return rows