from __future__ import annotations

import sqlite3
from pathlib import Path
from datetime import datetime

import pandas as pd

DB_PATH = Path("data/skillflow.db")


def init_db() -> None:
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS attempts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            test_id INTEGER NOT NULL,
            topic TEXT NOT NULL,
            status TEXT NOT NULL,
            self_score INTEGER NOT NULL,
            answer_text TEXT,
            created_at TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


def save_attempt(test_id: int, topic: str, status: str, self_score: int, answer_text: str) -> None:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO attempts (test_id, topic, status, self_score, answer_text, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (test_id, topic, status, self_score, answer_text, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    conn.commit()
    conn.close()


def load_attempts() -> pd.DataFrame:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    try:
        df = pd.read_sql_query("SELECT * FROM attempts ORDER BY created_at DESC", conn)
    finally:
        conn.close()
    return df


def clear_attempts() -> None:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("DELETE FROM attempts")
    conn.commit()
    conn.close()
