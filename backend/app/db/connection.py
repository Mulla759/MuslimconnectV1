import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent.parent.parent.parent / "db" / "database.db"

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    conn = get_connection()
    try:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS organizations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                verified INTEGER NOT NULL DEFAULT 0,
                category TEXT NOT NULL DEFAULT 'general',
                bio TEXT,
                followers INTEGER NOT NULL DEFAULT 0,
                event_count INTEGER NOT NULL DEFAULT 0
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

            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                campus TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            );

            INSERT OR IGNORE INTO organizations (id, name, verified, category, bio, followers, event_count)
            VALUES
                (1, 'Muslim Student Association', 1, 'msa', 'The heart of Muslim student life on campus. Weekly halaqas, Friday prayers, community dinners, and interfaith events.', 324, 12),
                (2, 'Islamic Society', 0, 'msa', 'A welcoming space for Muslim students to gather, worship, and grow together on campus.', 180, 8),
                (3, 'Al-Noor Cultural Society', 1, 'cultural', 'Celebrating the rich diversity of Muslim cultures through food festivals, art exhibitions, poetry nights, and heritage events.', 186, 8),
                (4, 'Islamic Knowledge Circle', 0, 'academic', 'Deep-dive study sessions on Quran, Hadith, Fiqh, and Islamic history. Open to all knowledge levels.', 142, 15),
                (5, 'Crescent Athletics', 0, 'sports', 'Building brotherhood and sisterhood through sports. Soccer leagues, basketball tournaments, hiking trips, and fitness challenges.', 98, 6),
                (6, 'Sisters of Light', 1, 'service', 'Empowering Muslim women through mentorship, community service, food drives, and outreach programs.', 267, 10),
                (7, 'Muslim Professionals Network', 0, 'professional', 'Career workshops, resume reviews, networking mixers, and industry panels connecting Muslim students with professionals.', 189, 4),
                (8, 'Quran Study Group', 0, 'academic', 'Weekly Quran recitation, tajweed practice, tafseer discussions, and memorization circles for all skill levels.', 156, 20),
                (9, 'Dawah Outreach Team', 1, 'dawah', 'Sharing Islam with compassion and clarity. Tabling events, informational booths, interfaith dialogues, and new Muslim support.', 211, 9),
                (10, 'Halal Foodies Club', 0, 'cultural', 'Exploring the best halal food spots, hosting potlucks, cooking workshops, and restaurant review nights.', 73, 3);

            INSERT OR IGNORE INTO events (id, organization_id, title, description, location, start_datetime, end_datetime, status)
            VALUES
                (1, 1, 'Annual MSA Gala Night 2026', 'Community dinner, keynote speakers, and student awards.', 'University Ballroom, Main Campus', '2026-04-10T19:00:00', '2026-04-10T22:00:00', 'scheduled'),
                (2, 1, 'Quran Study Circle', 'Weekly halaqah open to all students.', 'MSA Room 204', '2026-04-12T17:00:00', '2026-04-12T18:30:00', 'scheduled'),
                (3, 2, 'Iftar Gathering', 'Community iftar open to all.', 'Student Union Hall', '2026-04-15T19:30:00', '2026-04-15T21:00:00', 'scheduled');
        """)
        conn.commit()
    finally:
        conn.close()