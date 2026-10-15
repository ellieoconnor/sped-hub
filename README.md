# SpEd Hub

A tool for special education teachers that keeps their students' goals, goal tracking, and IEP info in one place, so they can track student progress without juggling multiple tools.

## Tech stack

- Frontend: React / TypeScript (not started yet)
- Backend: Python (FastAPI)
- Database: PostgreSQL (plain SQL via psycopg)

## Running it locally

### 1. Start Postgres

```
brew services start postgresql@17
```

### 2. Load the schema

This drops and recreates all tables, so it also resets the database.

```
/opt/homebrew/opt/postgresql@17/bin/psql sped_hub -f schema.sql
```

To look around inside the database, run `/opt/homebrew/opt/postgresql@17/bin/psql sped_hub`. Useful commands there: `\dt` (list tables), `\d tablename` (describe one), `\q` (quit).

### 3. Start the API

```
source .venv/bin/activate
fastapi dev main.py
```

Then open http://127.0.0.1:8000/docs to see the auto-generated API docs.

## Checking the database connection

With the virtual environment active:

```
python try_db.py
```

It prints the number of rows in `teachers`, for example `Total rows: (0,)`.

## Project files

- `main.py`: the FastAPI app
- `schema.sql`: all 8 tables (drops and recreates them)
- `try_db.py`: a scratch script that checks Python can reach Postgres