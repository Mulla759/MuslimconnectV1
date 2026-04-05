import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent.parent.parent / "db" / "database.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db() -> None:
    conn = get_connection()
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS organizations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                verified INTEGER NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                organization_id INTEGER NOT NULL REFERENCES organizations(id),
                title TEXT NOT NULL,
                description TEXT,
                location TEXT NOT NULL,
                start_datetime TEXT NOT NULL,
                end_datetime TEXT,
                status TEXT NOT NULL DEFAULT 'scheduled'
            );

            INSERT OR IGNORE INTO organizations (id, name, verified)
            VALUES
                (1, 'Muslim Student Association', 1),
                (2, 'Islamic Society', 0);

            INSERT OR IGNORE INTO events (
                id,
                organization_id,
                title,
                description,
                location,
                start_datetime,
                end_datetime,
                status
            )
            VALUES
                (
                    1,
                    1,
                    'Annual MSA Gala Night 2026',
                    'Community dinner, keynote speakers, and student awards.',
                    'University Ballroom, Main Campus',
                    '2026-04-10T19:00:00',
                    '2026-04-10T22:00:00',
                    'scheduled'
                ),
                (
                    2,
                    1,
                    'Quran Study Circle',
                    'Weekly halaqah open to all students.',
                    'MSA Room 204',
                    '2026-04-12T17:00:00',
                    '2026-04-12T18:30:00',
                    'scheduled'
                ),
                (
                    3,
                    2,
                    'Iftar Gathering',
                    'Community iftar open to all.',
                    'Student Union Hall',
                    '2026-04-15T19:30:00',
                    '2026-04-15T21:00:00',
                    'scheduled'
                );
            """
        )
        conn.commit()
    finally:
        conn.close()
