from db.database import get_connection
from repos.orgs import is_org_admin

def create_event(admin_user_id, org_id, payload):
    # check prehadn that the person making event request is asctually an admin for that specific org
    if not is_org_admin(org_id, admin_user_id):
        raise PermissionError("USER is not an admin of this organization")
    
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute(""" 
            INSERT INTO events (
                    organization_id, title, description, location, 
                    start_datetime, end_datetime, status
                    )
                VALUES (?,?,?,?,?,?,?)
            """,
            (
                org_id,
                payload['title'],
                payload.get("description"),
                payload["location"],
                payload["start_datetime"],
                payload.get("end_datetime"),
                payload.get("status","scheduled"),
            )
                    )
        conn.commit()
        return cur.lastrowid
    
    finally:
        conn.close()


def list_upcoming_events(limit=25):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
                    
            SELECT e.*, o.name AS organization_name
            FROM events e
            JOIN organizations o ON o.id = e.organization_id
            WHERE e.status != 'cancelled'
            ORDER BY e.start_datetime ASC
            LIMIT ? 
                """,
                (limit,),
        )
        return [dict(r) for r in cur.fetchall()]
    finally:
        conn.close()


