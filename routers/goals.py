import psycopg
from fastapi import APIRouter, HTTPException
from psycopg.rows import dict_row

from config import CURRENT_TEACHER_ID
from models import GoalCreate, GoalUpdate

router = APIRouter(tags=["goals"])

# GET all of one student's goals
@router.get("/students/{student_id}/goals")
def list_student_goals(student_id: int):
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        # check the student belongs to the current teacher
        student = conn.execute(
            "SELECT * FROM students WHERE teacher_id = %s AND student_id = %s",
            (CURRENT_TEACHER_ID, student_id),
        ).fetchone()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        # select the goals where student id matches the selected student
        goals = conn.execute(
            "SELECT * FROM student_goals WHERE student_id = %s",
            (student_id,),
        ).fetchall()
    return goals

# GET one student goal
@router.get("/goals/{goal_id}")
def get_student_goal(goal_id: int):
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        # goal -> student -> teacher
        goal = conn.execute(
            """
            SELECT student_goals.*
            FROM student_goals
            JOIN students ON students.student_id = student_goals.student_id
            WHERE student_goals.goal_id = %s
              AND students.teacher_id = %s
            """,
            (goal_id, CURRENT_TEACHER_ID),
        ).fetchone()

    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal

# POST — add a goal to a student
@router.post("/students/{student_id}/goals", status_code=201)
def create_student_goal(student_id: int, new_goal: GoalCreate):
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        # make sure student exists and is correct
        student = conn.execute(
            "SELECT * FROM students WHERE teacher_id = %s AND student_id = %s",
            (CURRENT_TEACHER_ID, student_id),
        ).fetchone()
        if not student:
            raise HTTPException(status_code=404, detail="Student not found")

        goal = conn.execute(
            """
            INSERT INTO student_goals (
                student_id,
                category_id,
                goal_text,
                baseline_value,
                baseline_notes,
                target_value,
                target_notes,
                start_date,
                due_date
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *
            """,
            (
                student_id,
                new_goal.category_id,
                new_goal.goal_text,
                new_goal.baseline_value,
                new_goal.baseline_notes,
                new_goal.target_value,
                new_goal.target_notes,
                new_goal.start_date,
                new_goal.due_date,
            ),
        ).fetchone()
    return goal

# PATCH — edit a goal
@router.patch("/goals/{goal_id}")
def update_goal(goal_id: int, changes: GoalUpdate):
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        goal = conn.execute(
            """
            UPDATE student_goals
            SET
                category_id = COALESCE(%s, category_id),
                goal_text = COALESCE(%s, goal_text),
                baseline_value = COALESCE(%s, baseline_value),
                baseline_notes = COALESCE(%s, baseline_notes),
                target_value = COALESCE(%s, target_value),
                target_notes = COALESCE(%s, target_notes),
                start_date = COALESCE(%s, start_date),
                due_date = COALESCE(%s, due_date)
            WHERE goal_id = %s
              AND student_id IN (SELECT student_id FROM students WHERE teacher_id = %s)
            RETURNING *
            """,
            (
                changes.category_id,
                changes.goal_text,
                changes.baseline_value,
                changes.baseline_notes,
                changes.target_value,
                changes.target_notes,
                changes.start_date,
                changes.due_date,
                goal_id,
                CURRENT_TEACHER_ID,
            ),
        ).fetchone()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal

# DELETE — delete one goal
@router.delete("/goals/{goal_id}", status_code=204)
def delete_goal(goal_id: int):
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        goal = conn.execute(
            """
            DELETE FROM student_goals
            WHERE goal_id = %s
              AND student_id IN (SELECT student_id FROM students WHERE teacher_id = %s)
            RETURNING goal_id
            """,
            (goal_id, CURRENT_TEACHER_ID),
        ).fetchone()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")