DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    user_id TEXT PRIMARY KEY,
    password TEXT NOT NULL
);

DROP TABLE IF EXISTS events;

CREATE TABLE events 
(
    event_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    date TEXT NULL ,
    start_time TEXT NULL,
    end_time TEXT NULL,
    description TEXT NOT NULL
);
INSERT INTO events (name, date, start_time, end_time, description)
VALUES
  ('Assignments', NULL, NULL, NULL, 'So you dont miss those deadlines'),
  ('Exams', NULL, NULL, NULL, 'To make sure you are ready for the big day.'),
  ('Hobbies', NULL, NULL, NULL, 'To keep up doing the things you love.'),
  ('Social', NULL, NULL, NULL, 'To schedule sometime for friends and family.'),
  ('To-Do', NULL, NULL, NULL, 'Tasks you cannot afford to forget about.'),
  ('Special', NULL, NULL, NULL, 'Special occasions.');

DROP TABLE IF EXISTS user_data;

CREATE TABLE user_data 
(
    user_id TEXT PRIMARY KEY,
    event_id INTEGER NOT NULL
);


