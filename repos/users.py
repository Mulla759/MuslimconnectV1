from db.database import get_connection




def create_user(email, full_name):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO user (email, full_name) VALUES (?,?)", (email, full_name), 
                    )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()



def get_user_by_email(email):
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE email =?", (email,))
        row = cur.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()



