from db.database import init_db
from repos.users import create_user
from repos.orgs import create_organization, add_org_admin
from repos.events import create_event, list_upcoming_events

def main():
    init_db()
    print("Database Initialized")

    #variablize user_id-> pass into create_user func 
    # variablize org_id -> use create_organization func
    # use org id and user id to add to org admins list

        # make a create_event call
            #user id,
            # org_id,
                #{
                #title:
                # description:
                # loco
                # start_datetime
                #}
        
    # print list of events

# if __name__ == "__main__":
#     main()



# --------- SCRAP ------
# def create_user(username):
#     conn = get_connection()
#     cursor = conn.cursor()

#     cursor.execute("INSERT INTO users (username) VALUES (?)", (username))
#     conn.commit()
#     user_id = cursor.lastrowid
#     conn.close()
#     return user_id