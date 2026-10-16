import psycopg
from fastapi import FastAPI
from psycopg.rows import dict_row

app = FastAPI()

# Define the endpoint and return the dictionary
@app.get("/")
def read_root():
    return {"message": "hello"}

# GET all students for a teacher
@app.get("/students")
def list_students():
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        rows = conn.execute("SELECT * FROM students WHERE teacher_id = 2").fetchall()
    return rows

# GET all teachers
@app.get("/teachers")
def list_teachers():
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        rows = conn.execute("SELECT first_name, last_name FROM teachers").fetchall()
    return rows