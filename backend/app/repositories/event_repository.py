"""SQLite data access for event queries."""
from app.db.connection import get_connection


def get_upcoming_events(limit: int) -> list[dict]:
    """Read non-cancelled events joined with organization metadata."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                e.id,
                e.organization_id,
                o.name AS organization_name,
                o.is_verified AS organization_verified,
                e.title,
                e.description,
                e.location,
                e.start_datetime,
                e.end_datetime,
                e.status
            FROM events e
            INNER JOIN organizations o ON o.id = e.organization_id
            WHERE e.status != 'cancelled'
            ORDER BY e.start_datetime ASC
            LIMIT ?
            """,
            (limit,),
        )
        rows = cursor.fetchall()

    return [
        {
            "id": row["id"],
            "organization_id": row["organization_id"],
            "organization_name": row["organization_name"],
            "organization_verified": bool(row["organization_verified"]),
            "title": row["title"],
            "description": row["description"],
            "location": row["location"],
            "start_datetime": row["start_datetime"],
            "end_datetime": row["end_datetime"],
            "status": row["status"],
        }
        for row in rows
    ]
