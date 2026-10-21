DROP TABLE IF EXISTS scores;
DROP TABLE IF EXISTS student_goals;
DROP TABLE IF EXISTS goal_bank;
DROP TABLE IF EXISTS student_disabilities;
DROP TABLE IF EXISTS goal_categories;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS teachers;
DROP TABLE IF EXISTS disabilities;

CREATE TABLE disabilities (
    disability_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE teachers (
    teacher_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email_address TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL 
);

CREATE TABLE students (
    student_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    teacher_id INTEGER NOT NULL REFERENCES teachers (teacher_id),
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    grade_level TEXT NOT NULL,
    birth_date DATE NOT NULL,
    accommodations TEXT NOT NULL,
    last_iep_date DATE,
    next_iep_date DATE
);

CREATE TABLE goal_categories (
    category_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    domain TEXT NOT NULL,
    skill TEXT
);

CREATE TABLE student_disabilities (
    student_id INTEGER NOT NULL REFERENCES students (student_id),
    disability_id INTEGER NOT NULL REFERENCES disabilities (disability_id),
    is_primary BOOLEAN NOT NULL,
    PRIMARY KEY (student_id, disability_id)
);

CREATE TABLE goal_bank (
    goal_bank_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    teacher_id INTEGER REFERENCES teachers (teacher_id),
    category_id INTEGER NOT NULL REFERENCES goal_categories (category_id),
    goal_text TEXT NOT NULL,
    is_stock BOOLEAN NOT NULL
);

CREATE TABLE student_goals (
    goal_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    student_id INTEGER NOT NULL REFERENCES students (student_id),
    category_id INTEGER NOT NULL REFERENCES goal_categories (category_id),
    goal_text TEXT NOT NULL,
    baseline_value NUMERIC,
    baseline_notes TEXT,
    target_value NUMERIC,
    target_notes TEXT,
    start_date DATE,
    due_date DATE NOT NULL,
    CHECK(target_value IS NOT NULL OR target_notes IS NOT NULL)
);

CREATE TABLE scores (
    score_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    goal_id INTEGER NOT NULL REFERENCES student_goals (goal_id),
    date DATE NOT NULL,
    value NUMERIC,
    notes TEXT,
    CHECK (value IS NOT NULL OR notes IS NOT NULL)
);