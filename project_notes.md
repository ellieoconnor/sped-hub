# Project Notes

## Stage 1

**Goal of Stage 1:** a working API where a teacher can add students, give them goals, and log scores, all saved in Postgres. Every endpoint does the same job: take a request, run a SQL query, return the result. So the skills are the same each time:

1. Python talks to Postgres (done: try_db.py)
2. Read data out (GET): run a SELECT and return rows as JSON. This is the next step, a GET /students endpoint.
3. Write data in (POST): run an INSERT with values from the request. This is where %s matters: those values come from users, so they must be passed as parameters or someone can run commands through your form. That’s why I brought it up early, but it belongs at this step.
4. Check the data with Pydantic models, which handle the cleaning and validating you asked about.
5. Auth, so each teacher only sees their own students.
6. The React UI on top.

## 15.10.2026 To-Do List

1. [x] Mock data. A seed.sql file with a couple of teachers, a few students, some goals and some scores. Done when you can re-run it and SELECT \* FROM students shows your fake students.
2. List students (GET /students). Done when opening the URL in your browser shows your seed students as JSON.
   One student (GET /students/{id}). Done when a real id returns that student and a made-up id returns a 404 instead of crashing.
3. Add a student (POST /students). Done when you can add a student from the /docs page, then see it in step 2’s list. This is where you learn parameterized SQL and input validation.
4. Edit and delete (PATCH, DELETE). Done when you can do all four actions on students from /docs. That’s full “CRUD”, a word interviewers use a lot.
5. Same pattern for goals, then scores. Done when you can give a seed student a goal and log three scores against it, all from /docs. This repeats steps 2 to 5, so it goes faster and shows you really learned the pattern.
6. Lookups (GET /categories, goal bank). Done when the dropdown data is there for the frontend to use.
7. Tidy up. Put the database connection in one shared place and add a few automated tests. Done when the tests pass with one command.
