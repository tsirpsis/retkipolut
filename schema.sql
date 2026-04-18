CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE destinations (
    id INTEGER PRIMARY KEY,
    title TEXT,
    content TEXT,
    creation_time TEXT,
    user_id INTEGER REFERENCES users
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY,
    content TEXT,
    sent_at TEXT,
    user_id INTEGER REFERENCES users ON DELETE CASCADE,
    destination_id INTEGER REFERENCES destinations ON DELETE CASCADE
);

CREATE TABLE destination_classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT,
    destination_id INTEGER REFERENCES destinations ON DELETE CASCADE
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE images (
    id INTEGER PRIMARY KEY,
    image BLOB,
    image_type TEXT,
    destination_id INTEGER REFERENCES destinations ON DELETE CASCADE
);
