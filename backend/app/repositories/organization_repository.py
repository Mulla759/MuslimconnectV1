from app.db.connection import get_connection


def fetch_all_organizations() -> list[dict]:
    conn = get_connection()
    try:
        cursor = conn.execute("""
            SELECT
                id,
                name,
                verified,
                category,
                bio,
                followers,
                event_count
            FROM organizations
            ORDER BY followers DESC
        """)
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()