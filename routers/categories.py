import psycopg
from fastapi import APIRouter
from psycopg.rows import dict_row

router = APIRouter(prefix="/goal-categories", tags=["goal-categories"])

# GET all goal categories
@router.get("")
def list_goal_categories():
    with psycopg.connect("dbname=sped_hub", row_factory=dict_row) as conn:
        categories = conn.execute(
            """
            SELECT * 
            FROM goal_categories 
            ORDER BY category_id ASC
            """
        ).fetchall()
    return categories