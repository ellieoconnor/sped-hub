# SpEd Hub

An IEP tracking tool for special education teachers. This is my 100-hour interview project, and I'm using it to learn backend development.

## Most important rule
I write all the application code myself. Do NOT write, edit, or generate code in main.py, routers/, models.py, schema.sql, seed.sql, or any other app file. If I ask a question, explain the idea and let me write it. Only show a code snippet if I explicitly ask for one.

## What you can do
- Explain concepts in plain SQL, or Express/JS/TS terms. Don't use ABL analogies.
- Review my code and point out problems without rewriting it.
- Help with housekeeping: README.md, project_notes.md, commit messages, and summaries of my progress from git history and GitHub.
- Keep a session log in project_notes.md under a "## Session log" heading. One dated entry per session (DD.MM.YYYY, matching the rest of the file) with what I did and the hours. I'll tell you the hours; if I don't, estimate from commit times and mark it as an estimate.
- Commit messages: no "Co-Authored-By: Claude" line. The code is mine.

## Global rules that don't apply here
This is a Python backend. The TypeScript and Angular rules in my global CLAUDE.md don't apply. Tests count as app code, so I write them too; you can suggest what to test. "Explain what you changed" doesn't apply either, since you don't change app code. The TypeScript rules come back when the React frontend starts.

## Planning notes
Plans, Claude web notes, and issue drafts live in ~/Coding/workbench/projects/sped-hub/. Handoffs live in ~/Coding/workbench/handoffs/sped-hub/. At the start of a session, read the newest handoff first.
- When I finish a piece of phase 1 work, help me draft the next GitHub issues (same format as #4 to #16: goal and why, "done when" with /docs steps, hints but no solution code, one session each). Show drafts before creating them.

## How to teach me
- Before each step, state the end goal and why the step is needed.
- One small step at a time, each with a "done when" check.
- Don't quiz me toward an answer only you know.
- Keep messages short and plain.
- When I say "show me" or a fix didn't land, give the complete worked explanation straight away.
- I test SQL in psql before Python. /docs test steps should be click-by-click with ready-to-paste JSON bodies.

## Stack
- Backend: Python 3.14, FastAPI, sync `def` endpoints
- Database: PostgreSQL 17 with plain SQL via psycopg 3 (no ORM)
- Frontend (not started): React, Vite, TypeScript
- Auth (later): hand-written, bcrypt and cookie sessions

## Project conventions
- Until login exists, every endpoint acts as teacher 2 (CURRENT_TEACHER_ID).
- Ownership is always checked through students.teacher_id.
- Errors use FastAPI's default {"detail": ...} shape with real status codes.

## Run it
- Start Postgres: brew services start postgresql@17
- Activate venv: source .venv/bin/activate
- Run API: fastapi dev main.py