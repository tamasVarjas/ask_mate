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
                    SELECT answer.id, answer.message, question.title
                    FROM answer
                    JOIN question ON (question_id = question.id)
                    JOIN user_answer ON (answer_id = answer.id)
                    WHERE user_id = %(user_id)s; 
                   """,
                   {'user_id': user_id})
    answers = cursor.fetchall()
    
    return answers


@database_common.connection_handler
def get_comments_by_user(cursor, user_id):
    cursor.execute("""
                    SELECT comment.id, comment.message AS comment, question.title, answer.message
                    FROM comment
                    FULL JOIN question ON (comment.question_id = question.id)
                    FULL JOIN answer ON (comment.answer_id = answer.id)
                    JOIN user_comment ON (comment_id = comment.id)
                    WHERE user_id = %(user_id)s; 
                   """,
                   {'user_id': user_id})
    comments = cursor.fetchall()
    
    return comments
