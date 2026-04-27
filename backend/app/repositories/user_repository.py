from app.db.connection import get_connection


def get_user_by_email(email: str):
    conn = get_connection()
    try:
        row = conn.execute(
            "SELECT * FROM users WHERE email = ?", (email,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def create_user(first_name: str, last_name: str, email: str, password_hash: str, campus: str = None):
    conn = get_connection()
    try:
        cursor = conn.execute(
            """INSERT INTO users (first_name, last_name, email, password_hash, campus)
               VALUES (?, ?, ?, ?, ?)""",
            (first_name, last_name, email, password_hash, campus)
        )
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()
        