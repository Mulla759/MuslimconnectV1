from db.database import get_connection


def create_organization(name, official_email, is_verified = False):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO organizations (name, official_email, is_verified) VALUES (?,?,?)",
        (name, official_email, 1 if is_verified else 0),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()

def add_org_admin(org_id, user_id):
    conn = get_connection()
    try:
        cur= conn.cursor()
        cur.execute(
            "SELECT 1 FROM organization_admins WHERE organization_id = ? AND user_id =?", (org_id, user_id),
        )
        return cur.fetchone() is not None
    finally:
        conn.close()



