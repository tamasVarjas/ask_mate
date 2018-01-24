import database_common


@database_common.connection_handler
def get_all_user_data(cursor):
    cursor.execute("""
                    SELECT username, image FROM users
                    ORDER BY id;
                   """)
    users = cursor.fetchall()

    return users
