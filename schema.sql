CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE patterns (
    id INTEGER PRIMARY KEY,
    title TEXT,
    description TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    pattern_id INTEGER REFERENCES patterns,
    user_id INTEGER REFERENCES users,
    comment TEXT
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT,
    element TEXT
);

CREATE TABLE pattern_classes (
    id INTEGER PRIMARY KEY,
    pattern_id INTEGER REFERENCES patterns,
    title TEXT,
    value TEXT
);
