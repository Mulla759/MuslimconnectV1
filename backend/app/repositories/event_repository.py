from app.db.connection import get_connection


def fetch_upcoming_events(limit: int) -> list[dict]:
    conn = get_connection()
    try:
        cursor = conn.execute(
            """
            SELECT
                e.id,
                e.organization_id,
                o.name AS organization_name,
                o.verified AS organization_verified,
                e.title,
                e.description,
                e.location,
                e.start_datetime,
                e.end_datetime,
                e.status
            FROM events e
            JOIN organizations o ON o.id = e.organization_id
            WHERE e.status != 'cancelled'
            AND e.start_datetime >= datetime('now')
            ORDER BY e.start_datetime ASC
            LIMIT ?
            """,
            (limit,),
        )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()

def fetch_event_by_id(event_id: int) -> dict | None:
    conn = get_connection()
    try:
        row = conn.execute("""
            SELECT
                e.id,
                e.organization_id,
                o.name AS organization_name,
                o.verified AS organization_verified,
                e.title,
                e.description,
                e.location,
                e.start_datetime,
                e.end_datetime,
                e.status
            FROM events e
            JOIN organizations o ON o.id = e.organization_id
            WHERE e.id = ?
        """, (event_id,)).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

        