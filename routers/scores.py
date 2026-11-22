import psycopg
from fastapi import APIRouter, HTTPException
from psycopg.rows import dict_row

from config import CURRENT_TEACHER_ID
from models import ScoreCreate, ScoreUpdate

router = APIRouter(prefix="/goals/{goal_id}/", tags=["scores"])

# GET — list a goals's scores
# /goals/{goal_id}/scores
@router.get("")
def list_scores(goal_id: int):
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        scores = conn.execute("SELECT * FROM scores WHERE goal_id = %s", (goal_id,)).fetchall()
    return scores

# GET — view one score
# /goals/{goal_id}/scores/{score_id}
@router.get("/{score_id}")
def get_score(goal_id: int, score_id: int):
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        score = conn.execute(
            """
            SELECT * 
            FROM scores 
            JOIN student_goals ON student_goals.goal_id = scores.goal_id
            JOIN students ON students.student_id = student_goals.student_id
            WHERE scores.score_id= %s
                AND scores.goal_id = %s
                AND students.teacher_id = %s
            """, (score_id, goal_id, CURRENT_TEACHER_ID),
            ).fetchone()
    if not score:
        raise HTTPException(status_code=404, detail="Score not found")

    return score

# POST — add a score (no score_id yet)
# /goals/{goal_id}/scores
@router.post("", status_code=201)
def create_a_score(goal_id: int, new_score: ScoreCreate):
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        # make sure the goal exists and is correct
        goal = conn.execute(
            "SELECT * FROM student_goals WHERE goal_id = %s", (goal_id),
        ).fetchone()
        if not goal:
            raise HTTPException(status_code=404, detail="Goal not found")

        score = conn.execute(
            """
            INSERT INTO scores (
                goal_id,
                score_date,
                value,
                notes,
            )
            VALUES (%s, %s, %s, %s)
            RETURNING *
            """,
            (
                goal_id,
                new_score.score_date,
                new_score.value,
                new_score.notes
            ),
        ).fetchone()
    return score

# PATCH — edit a score
# /goals/{goal_id}/scores/{score_id}
@router.patch("/{score_id}")
def update_score(score_id: int, changes: ScoreUpdate):
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        score = conn.execute(
            """
            UPDATE scores
            SET
                goal_id = COALESCE(%s, goal_id),
                score_date = COALESCE(%s, score_date),
                value = COALESCE(%s, value),
                notes = COALESCE(%s, notes)
            WHERE score_id = %s
                AND student_id IN (SELECT student_id FROM students WHERE teacher_id = %s)
            RETURNING *
            """,
            (
                changes.goal_id,
                changes.score_date,
                changes.values,
                changes.notes,
                score_id,
                CURRENT_TEACHER_ID
            ),
        ).fetchone()
    if not score:
        raise HTTPException(status_code=404, detail="Score not found")
    raise score

# DELETE — delete a score
# /goals/{goal_id}/scores/{score_id}
@router.delete("/scores/{score_id}", status_code=204)
def delete_score(goal_id: int, score_id: int):
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        score = conn.execute(
            """
            DELETE FROM scores
            WHERE scores.score_id = %s
                AND scores.goal_id = %s
                AND scores.goal_id IN (
                    SELECT goal_id 
                    FROM student_goals 
                    WHERE student_id 
                    IN (
                        SELECT student_id 
                        FROM students 
                        WHERE teacher_id = %s
                    )
                )
            RETURNING score_id
            """,
            (score_id, goal_id, CURRENT_TEACHER_ID)
        ).fetchone()
    if not score:
        raise HTTPException(status_code=404, detail="Score not found")

# TODO: ADD TO ANKI RULE TO REMEMBER: 
# INSERT needs a check first; UPDATE and DELETE can check inside their WHERE.