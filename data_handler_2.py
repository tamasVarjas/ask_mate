import bcrypt
import database_common


def hash_password(plain_text_password):
    hashed_bytes = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())

    return hashed_bytes.decode('utf-8')


def verify_password(plain_text_password, hashed_password):
    hashed_bytes_password = hashed_password.encode('utf-8')

    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_bytes_password)


@database_common.connection_handler
def save_registration(cursor, username, password, image):
    cursor.execute("""
                    INSERT INTO users (username, password, image) 
                    VALUES (%(username)s, %(password)s, %(image)s);
                   """,
                   {'username': username, 'password': password, 'image': image})


@database_common.connection_handler
def save_registration_without_image(cursor, username, password):
    cursor.execute("""
                    INSERT INTO users (username, password) 
                    VALUES (%(username)s, %(password)s);
                   """,
                   {'username': username, 'password': password})


@database_common.connection_handler
def get_all_user_data(cursor):
    cursor.execute("""
                    SELECT username, image FROM users
                    ORDER BY id;
                   """)
    users = cursor.fetchall()

    return users


@database_common.connection_handler
def get_users_password(cursor, username):
    cursor.execute("""
                    SELECT password FROM users
                    WHERE username = %(username)s;
                   """,
                   {'username': username})
    password = cursor.fetchone()

    return password
  

@database_common.connection_handler
def get_all_username(cursor, username):
    cursor.execute("""
                    SELECT username FROM users
                    WHERE username = %(username)s;
                   """,
                {'username': username })
    username_search = cursor.fetchone()
    
    return username_search


@database_common.connection_handler
def get_questions_by_user(cursor, user_id):
    cursor.execute("""
                    SELECT id, title 
                    FROM question
                    JOIN user_question ON (question_id = id)
                    WHERE user_id = %(user_id)s; 
                   """,
                   {'user_id': user_id})
    questions = cursor.fetchall()

    return questions


@database_common.connection_handler
def get_answers_by_user(cursor, user_id):
    cursor.execute("""
                    SELECT answer.id, answer.message, question.title, question.id AS question_id
                    FROM answer
                    JOIN question ON (question_id = question.id)
                    JOIN user_answer ON (answer_id = answer.id)
                    WHERE user_id = %(user_id)s; 
                   """,
                   {'user_id': user_id})
    answers = cursor.fetchall()

    return answers


@database_common.connection_handler
def get_question_comments_by_user(cursor, user_id):
    cursor.execute("""
                    SELECT comment.id, comment.message AS comment, question.title, question.id AS question_id
                    FROM comment
                    
                    JOIN question ON (comment.question_id = question.id)
                    JOIN user_comment ON (comment_id = comment.id)
                    WHERE user_id = %(user_id)s; 
                   """,
                   {'user_id': user_id})
    question_comments = cursor.fetchall()

    return question_comments


@database_common.connection_handler
def get_answer_comments_by_user(cursor, user_id):
    cursor.execute("""
                    SELECT comment.id, comment.message AS comment,
                    answer.message,
                    question.id AS question_id, question.title AS title
                    FROM comment
                    FULL JOIN answer ON (comment.answer_id = answer.id)
                    INNER JOIN question ON (answer.question_id = question.id)
                    JOIN user_comment ON (comment_id = comment.id)
                    WHERE user_id = %(user_id)s; 
                   """,
                   {'user_id': user_id})
    answer_comments = cursor.fetchall()

    return answer_comments


@database_common.connection_handler
def get_users_image(cursor, username):
    cursor.execute("""
                    SELECT image FROM users
                    WHERE username = %(username)s;
                   """,
                   {'username': username})
    image = cursor.fetchone()

    return image

@database_common.connection_handler
def get_id_by_username(cursor, username):
    cursor.execute("""
                    SELECT id FROM users
                    WHERE username = %(username)s;
                    """,
                   {'username': username})
    id = cursor.fetchone()

    return id

@database_common.connection_handler
def get_profile_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT username, image 
                    FROM users
                    JOIN user_question ON (user_id = users.id)
                    WHERE question_id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    profile = cursor.fetchone()

    return profile


@database_common.connection_handler
def get_answer_profile_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT users.username, users.image 
                    FROM users
                    JOIN user_answer ON (user_id = users.id)
                    JOIN answer ON (answer_id = answer.id)
                    WHERE question_id = %(question_id)s
                    GROUP BY users.username, users.image;
                    """,
                   {'question_id': question_id})
    profile = cursor.fetchall()

    return profile

@database_common.connection_handler
def get_comment_answer_profile_by_answer_id(cursor, answer_id):
    cursor.execute("""
                    SELECT users.username, users.image 
                    FROM users
                    JOIN user_comment ON (user_id = users.id)
                    JOIN comment ON (comment_id = comment.id)
                    WHERE comment.answer_id = %(answer_id)s;
                    """,
                   {'answer_id': answer_id})
    profile = cursor.fetchall()

    return profile

@database_common.connection_handler
def get_comment_answer_profile_by_question_id(cursor, question_id):
    cursor.execute("""
                    SELECT users.username, users.image 
                    FROM users
                    JOIN user_comment ON (user_id = users.id)
                    JOIN comment ON (comment_id = comment.id)
                    WHERE comment.question_id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    profile = cursor.fetchall()

    return profile