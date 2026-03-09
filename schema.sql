-- This SQL script sets up the database schema for the Fifty-Two Pickup game.

-- The `users` table stores information about each registered user, including their username, email, password hash, and the timestamp of when they created their account.
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- This table stores each attempt a user makes at recalling the shuffled deck.
CREATE TABLE attempts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    deck_order  TEXT NOT NULL,
    recall_order TEXT,
    accuracy REAL NOT NULL,
    duration_seconds REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);