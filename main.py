import psycopg
from fastapi import FastAPI
from psycopg.rows import dict_row

app = FastAPI()


# Define the endpoint and return the dictionary
@app.get("/")
def read_root():
    return {"message": "hello"}

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

# GET all teachers
@app.get("/teachers")
def list_teachers():
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        rows = conn.execute("SELECT first_name, last_name FROM teachers").fetchall()
    return rows