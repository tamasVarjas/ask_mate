import database_common

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
                    SELECT comment.id, comment.message, question.title, answer.message
                    FROM comment
                    FULL JOIN question ON (comment.question_id = question.id)
                    FULL JOIN answer ON (comment.answer_id = answer.id)
                    JOIN user_comment ON (comment_id = comment.id)
                    WHERE user_id = %(user_id)s; 
                    """,
                   {'user_id': user_id})
    comments = cursor.fetchall()
    return comments