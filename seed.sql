insert into teachers (first_name, last_name, email_address, password_hash)
values ('Craig', 'Pelton', 'deanpelton@greendale.edu', 'password-for-ellie');

insert into teachers (first_name, last_name, email_address, password_hash)
values ('Ian', 'Duncan', 'iduncan@greendale.edu', 'password-for-ellie');

insert into teachers (first_name, last_name, email_address, password_hash)
values ('Ben', 'Chang', 'bchang@greendale.edu', 'password-for-ellie');


insert into students (teacher_id, first_name, last_name, grade_level, birth_date, accommodations, last_iep_date, next_iep_date)
values (2, 'Jeff', 'Winger', '9th', '2011-11-20', 'Extra time on tests, Can be in a separate room for tests, Guided notes', '2025-12-12', '2026-12-11');

insert into students (teacher_id, first_name, last_name, grade_level, birth_date, accommodations, last_iep_date, next_iep_date)
values (2, 'Garrett', 'Lambert', '9th', '2011-07-06', 'Extra time on tests, Tests read to student, May take breaks to re-regulate', '2026-09-03', NULL);

insert into students (teacher_id, first_name, last_name, grade_level, birth_date, accommodations, last_iep_date, next_iep_date)
values (3, 'Annie', 'Edison', '5th', '2015-02-20', 'Notes for tests, May answer written assessments orally', '2026-03-14', '2027-03-11');