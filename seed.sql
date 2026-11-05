--TEACHER SEED DATA
insert into teachers (first_name, last_name, email_address, password_hash)
values ('Craig', 'Pelton', 'deanpelton@greendale.edu', 'password-for-ellie');

insert into teachers (first_name, last_name, email_address, password_hash)
values ('Ian', 'Duncan', 'iduncan@greendale.edu', 'password-for-ellie');

insert into teachers (first_name, last_name, email_address, password_hash)
values ('Ben', 'Chang', 'bchang@greendale.edu', 'password-for-ellie');

-- STUDENT SEED DATA
insert into students (teacher_id, first_name, last_name, grade_level, birth_date, accommodations, last_iep_date, next_iep_date)
values (2, 'Jeff', 'Winger', '9th', '2011-11-20', 'Extra time on tests, Can be in a separate room for tests, Guided notes', '2025-12-12', '2026-12-11');

insert into students (teacher_id, first_name, last_name, grade_level, birth_date, accommodations, last_iep_date, next_iep_date)
values (2, 'Garrett', 'Lambert', '9th', '2011-07-06', 'Extra time on tests, Tests read to student, May take breaks to re-regulate', '2026-09-03', NULL);

insert into students (teacher_id, first_name, last_name, grade_level, birth_date, accommodations, last_iep_date, next_iep_date)
values (3, 'Annie', 'Edison', '5th', '2015-02-20', 'Notes for tests, May answer written assessments orally', '2026-03-14', '2027-03-11');

-- GOAL CATEGORY SEED DATA (ids become 1, 2, 3)
insert into goal_categories (domain, skill)
values ('Reading', 'Comprehension');

insert into goal_categories (domain, skill)
values ('Math', 'Computation');

insert into goal_categories (domain, skill)
values ('Behaviour', 'On-task');

-- STUDENT GOAL SEED DATA
insert into student_goals (student_id, category_id, goal_text, baseline_value, baseline_notes, target_value, target_notes, start_date, due_date)
values (1, 1, 'A reading comprehension goal text example', 40, NULL, 80, NULL, NULL, '2026-12-12');

insert into student_goals (student_id, category_id, goal_text, baseline_value, baseline_notes, target_value, target_notes, start_date, due_date)
values (1, 3, 'When given a new task, Jeff will start task promptly, remain on task without being reminded, continue working until task is complete, on 4/5 incidents by following all 4 steps with 100% accuracy.', NULL, 'Current baseline is 2/5', NULL, '4/5 incidents following all 4 steps with 100% accuracy', NULL, '2026-12-12');

insert into student_goals (student_id, category_id, goal_text, baseline_value, baseline_notes, target_value, target_notes, start_date, due_date)
values (3, 2, 'A math computation goal', 40, NULL, 80, NULL, NULL, '2026-12-12');