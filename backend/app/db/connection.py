"""SQLite connection utilities and lightweight bootstrap seeding."""
from pathlib import Path
import sqlite3

from app.config.settings import settings


def _resolve_database_path() -> Path:
    """Resolve a project-root-relative SQLite path from settings."""
    root = Path(__file__).resolve().parents[3]
    return (root / settings.database_url).resolve()


def get_connection() -> sqlite3.Connection:
    """Create a SQLite connection with row access by column name."""
    database_path = _resolve_database_path()
    database_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(database_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def ensure_initialized() -> None:
    """Create required tables and seed one example event for handoff use."""
    with get_connection() as conn:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS organizations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL UNIQUE,
                official_email TEXT,
                is_verified INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                organization_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                location TEXT NOT NULL,
                start_datetime TEXT NOT NULL,
                end_datetime TEXT,
                status TEXT NOT NULL DEFAULT 'scheduled',
                created_at TEXT NOT NULL DEFAULT (datetime('now')),
                FOREIGN KEY (organization_id) REFERENCES organizations(id) ON DELETE CASCADE
            );

            CREATE INDEX IF NOT EXISTS idx_events_start ON events(start_datetime);
            """
        )

        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) AS count FROM organizations")
        org_count = cursor.fetchone()["count"]
        if org_count == 0:
            cursor.execute(
                """
                INSERT INTO organizations (name, official_email, is_verified)
                VALUES (?, ?, ?)
                """,
                ("Muslim Student Association", "msa@umn.edu", 1),
            )
            org_id = cursor.lastrowid
            cursor.execute(
                """
                INSERT INTO events (
                    organization_id,
                    title,
                    description,
                    location,
                    start_datetime,
                    end_datetime,
                    status
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    org_id,
                    "Annual MSA Gala Night 2026",
                    "Community dinner, keynote speakers, and student awards.",
                    "University Ballroom, Main Campus",
                    "2026-04-10T19:00:00",
                    "2026-04-10T22:00:00",
                    "scheduled",
                ),
            )

        conn.commit()
