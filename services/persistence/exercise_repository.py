import sqlite3
import streamlit as st
from pathlib import Path

_DB_PATH = str(Path(__file__).parent.parent.parent / "data.db")


@st.cache_resource
def _get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = _get_connection()

    with conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                username   TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS exercises (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id       INTEGER NOT NULL REFERENCES users(id),
                exercise_name TEXT    NOT NULL,
                reps          INTEGER NOT NULL DEFAULT 0,
                sets          INTEGER NOT NULL DEFAULT 0,
                time          INTEGER NOT NULL DEFAULT 0,
                created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def get_user(username: str) -> sqlite3.Row:
    conn = _get_connection()
    return conn.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    ).fetchone()


def create_user(username: str) -> sqlite3.Row:
    conn = _get_connection()

    with conn:
        conn.execute(
            "INSERT INTO users (username) VALUES (?)", (username,)
        )

    return get_user(username)


def get_or_create_user(username: str) -> sqlite3.Row:
    user = get_user(username)

    if user is None:
        user = create_user(username)

    return user


from datetime import datetime, timezone, timedelta

IST = timezone(timedelta(hours=5, minutes=30))

def get_ist_now():
    return datetime.now(IST).strftime("%Y-%m-%d %H:%M:%S")

def get_ist_date():
    return datetime.now(IST).strftime("%Y-%m-%d")


def add_exercise(user_id, exercise_name, reps, sets, duration):  # ← time → duration
    conn = _get_connection()
    today_ist = get_ist_date()

    with conn:
        existing = conn.execute("""
            SELECT * FROM exercises 
            WHERE user_id = ? AND exercise_name = ? AND Date(created_at) = ?
        """, (user_id, exercise_name, today_ist)).fetchone()  # ← fixed Date('created_at') and Date('now')

        if existing:
            conn.execute("""
                UPDATE exercises 
                SET reps = reps + ?, sets = sets + ?, time = time + ?
                WHERE id = ?
            """, (reps, sets, duration, existing['id']))  # ← time → duration

        else:
            conn.execute("""
                INSERT INTO exercises (user_id, exercise_name, sets, reps, time, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user_id, exercise_name, sets, reps, duration, get_ist_now()))  # ← time → duration, added created_at


def get_users_exercises(user_id):
    conn = _get_connection()
    return conn.execute("""
        SELECT * FROM exercises 
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,)).fetchall()  # ← added ORDER BY