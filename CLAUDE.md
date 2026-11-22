# SpEd Hub

An IEP tracking tool for special education teachers. This is my 100-hour interview project. I'm a frontend dev (JavaScript/TypeScript, Express) using it to learn backend, and I want to explain every part of it confidently in interviews.

## Most important rule
I write all the application code myself. Do NOT write, edit, or generate code in main.py, config.py, models.py, routers/, schema.sql, seed.sql, tests, or any other app file. You can read any file and run read-only commands (psql `SELECT`, `\d table`, `git status`, starting the API) to see where I am. Don't guess. Check the real files first.

## What you can do
- Explain concepts in plain SQL, or Express/JS/TS terms ("`@router.get` is like `router.get('/x', handler)`"). Don't use ABL analogies.
- Review my code and point out problems without rewriting it.
- Help with housekeeping: README.md, project_notes.md, commit messages, and summaries of my progress from git history and GitHub.
- To-do list: when a to-do's "done when" check passes, tick its box in project_notes.md. Nothing else. No session log.
- When we finish a milestone, remind me to commit.
- Offer an Anki-style Q/A card for key new ideas.
- Don't propose extra documentation steps.
- Commit messages: no "Co-Authored-By: Claude" line. The code is mine.

## How to teach me
- I want to work from my to-do list and problem-solve myself. Help when I ask. Don't direct every step or run ahead.
- Before each step, state the end goal and why the step is needed.
- One small step at a time, each with a "done when" check.
- Don't quiz me toward an answer only you know.
- Keep messages short and plain.
- When I say "show me" or a fix didn't land: give the exact before/after lines and I type them. If that still doesn't work, or I say "just give me the whole function", give the complete paste-ready function.
- When I'm stuck on something new, a complete worked example on a different table that I then adapt works well.
- I test SQL in psql before Python. /docs test steps should be click-by-click (which section, Try it out, which values, Execute, the status code and body I should see) with ready-to-paste JSON bodies.

## Global rules that don't apply here
This is a Python backend. The TypeScript and Angular rules in my global CLAUDE.md don't apply. Tests count as app code, so I write them too; you can suggest what to test. "Explain what you changed" doesn't apply either, since you don't change app code. The TypeScript rules come back when the React frontend starts.

## Planning notes
Plans, Claude web notes, and issue drafts live in ~/Coding/workbench/projects/sped-hub/. Handoffs live in ~/Coding/workbench/handoffs/sped-hub/. At the start of a session, read the newest handoff first.
- When I finish a piece of phase 1 work, help me draft the next GitHub issues (same format as #4 to #16: goal and why, "done when" with /docs steps, hints but no solution code, one session each). Show drafts before creating them.

## Stack
- Backend: Python 3.14, FastAPI, sync `def` endpoints (the driver is sync)
- Database: PostgreSQL 17 with plain SQL via psycopg 3: `%s` parameters, `row_factory=dict_row`, no ORM
- Pydantic models live in models.py (StudentCreate/Update, GoalCreate/Update, ScoreCreate/Update)
- Frontend (not started): React, Vite, TypeScript
- Auth (later): hand-written, bcrypt and cookie sessions

## Project layout and conventions
- main.py is just the app. It imports each router and calls `app.include_router(...)`.
- routers/students.py (prefix `/students`), routers/goals.py (no prefix: `/students/{student_id}/goals` and `/goals/{goal_id}`), routers/scores.py (prefix `/goals/{goal_id}/scores`).
- Function names: `list_x`, `get_x`, `create_x`, `update_x`, `delete_x`. Results named `student` / `students` etc.
- Triple-quoted multi-line SQL.
- Errors use FastAPI's default `{"detail": ...}` shape with real status codes (404 not found, 201 created, 204 deleted).
- PATCH style: every column `col = COALESCE(%s, col)`, with an Update model where every field is `| None = None`. Known limit: you can't set a field back to NULL. Later (milestone 8): build SET from only the sent fields (`model_dump(exclude_unset=True)` + `psycopg.sql.Identifier`).
- `psycopg.connect` is repeated in each function for now. A shared helper comes in milestone 8.

## Ownership (the important pattern)
Until login exists, every endpoint acts as teacher 2 (Duncan) via `CURRENT_TEACHER_ID` in config.py. At login it becomes the session teacher's id, never something from the URL.

Only `students` has `teacher_id`. Everything else proves ownership through `students.teacher_id`:
- GETs and pre-checks: `JOIN students ON ... WHERE ... AND students.teacher_id = %s`
- PATCH/DELETE on goals: `AND student_id IN (SELECT student_id FROM students WHERE teacher_id = %s)`
- PATCH/DELETE on scores: `AND scores.goal_id IN (SELECT goal_id FROM student_goals WHERE student_id IN (SELECT student_id FROM students WHERE teacher_id = %s))`
- INSERT needs a check first (POST score checks the goal). UPDATE and DELETE check inside their WHERE.
- Recipe: FROM the table you want, one condition per id in the URL, then go up the chain to `students.teacher_id`.
- Something you don't own gives 404, the same as not existing.

## Seed data (seed.sql)
- Teachers: 1 Pelton (no students, to test empty lists), 2 Duncan (current teacher), 3 Chang
- Students: 1 Jeff and 2 Garrett (teacher 2), 3 Annie (teacher 3, for 404 tests). Garrett has no goals (empty-list test).
- goal_categories: 1 Reading/Comprehension, 2 Math/Computation, 3 Behaviour/On-task
- Goals: 1 (numeric) and 2 (notes-only) for Jeff, 3 for Annie
- Scores: 1 to 3 on goal 1, 4 on goal 2 (notes-only), 5 on goal 3 (Annie)
- goal_bank: not seeded yet

## Tables (schema.sql is the truth)
- goal_categories: category_id, domain, skill (nullable)
- student_goals: goal_id, student_id, category_id, goal_text, baseline_value, baseline_notes, target_value, target_notes, start_date, due_date. CHECK: target_value or target_notes must be filled in.
- goal_bank: goal_bank_id, teacher_id (NULL for stock goals), category_id, goal_text, is_stock
- scores: score_id, goal_id, score_date (defaults to today), value (NUMERIC), notes. CHECK: value or notes must be filled in.

## The 8 API milestones
1. to 5. Students CRUD: done
6. Goals, then scores: done
7. **Lookups (current):**
   - **GET /goal-categories**: new routers/categories.py, prefix `/goal-categories`. Shared lookup data, so no ownership check and no URL ids. Done when /docs shows it and it returns the 3 categories.
   - **Goal bank** (`/goal-bank`): GET list (mine + stock: `teacher_id = %s OR is_stock`), POST (a bank goal owned by me, is_stock false), GET one, PATCH and DELETE (only my own, never stock goals). Needs seeding first. Talk me through the design before I write it.
   - Done when the dropdown data is ready for the frontend.
8. Tidy up: one shared db connection helper (db.py `get_conn()`, maybe a pool + `Depends` later), a few pytest tests (my /docs checks become tests), a clean 400 instead of 500 for a bad category_id or CHECK failure, decide CASCADE vs 409 for deleting a goal that has scores, PATCH option B. Done when the tests pass with one command.

## Run it (from ~/Coding/sped-hub)
- Start Postgres: `brew services start postgresql@17`
- psql: `psql sped_hub` (`\q` quits, `q` closes a wide result)
- Reset and reseed: `psql sped_hub -f schema.sql`, then `psql sped_hub -f seed.sql`
- Activate venv: `source .venv/bin/activate` (check with `which python`)
- Run API: `fastapi dev main.py` (reloads on save), then http://127.0.0.1:8000/docs

## Gotchas I've hit
- psql needs `;`. At a `-#` prompt, just type `;` (or `\r` to clear). Don't retype the query.
- SQL typed into zsh gives `command not found`. Open psql first.
- /docs pre-fills every body field with "string" or today's date. For PATCH, delete everything except the fields I'm changing.
- A one-item tuple needs a comma: `(goal_id,)`.
- Count the `%s` in a query. The tuple needs the same number of values, in the same order.
