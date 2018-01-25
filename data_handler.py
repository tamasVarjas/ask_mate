from datetime import datetime
import database_common
import data_handler_2

@database_common.connection_handler
def get_all_data(cursor, data_table):
    cursor.execute("""
                    SELECT * FROM """ + data_table + """
                    ORDER BY id;
                   """,
                   {'data_table': data_table})
    all_data = cursor.fetchall()
    return all_data


@database_common.connection_handler
def delete_question(cursor, question_id):
    cursor.execute("""
                    DELETE FROM question_tag
                    WHERE question_id = %(question_id)s;
                    DELETE FROM answer
                    WHERE question_id = %(question_id)s;
                    DELETE FROM question
                    WHERE id = %(question_id)s;
                    SELECT * FROM question;
                    """,
                   {'question_id': question_id})
    questions = cursor.fetchall()
    return questions


@database_common.connection_handler
def delete_answer(cursor, answer_id):
    cursor.execute("""
                    DELETE FROM answer
                    WHERE id = %(answer_id)s;
                    SELECT * FROM answer;
                    """,
                   {'answer_id': answer_id})
    answers = cursor.fetchall()
    return answers


@database_common.connection_handler
def get_answers(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE question_id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    answers = cursor.fetchall()
    return answers


@database_common.connection_handler
def add_new_question(cursor, title, message, image, tag, username):
    date_time = datetime.now()
    if image != '':
        cursor.execute("""
                        INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                        VALUES (%(date_time)s, 0, 0, %(title)s, %(message)s, %(image)s); 
                        """,
                       {'date_time': date_time, 'title': title, 'message': message, 'image': image})
    else:
        cursor.execute("""
                        INSERT INTO question (submission_time, view_number, vote_number, title, message)
                        VALUES (%(date_time)s, 0, 0, %(title)s, %(message)s); 
                        """,
                       {'date_time': date_time, 'title': title, 'message': message})
    add_new_tag(tag)
    last_question_id = get_last_question_id()
    tag_id = get_tag_id_by_tag_name(tag)
    user_id = data_handler_2.get_id_by_username(username)
    cursor.execute("""
                    INSERT INTO question_tag (question_id, tag_id) 
                    VALUES (%(last_question_id)s, %(tag_id)s);
                    """,
                   {'last_question_id': last_question_id['last_value'], 'tag_id': tag_id['id']})
    cursor.execute("""
                    INSERT INTO user_question (question_id, user_id)
                    VALUES (%(last_question_id)s, %(user_id)s)
                    """,
                   {'last_question_id': last_question_id['last_value'], 'user_id': user_id['id']})


@database_common.connection_handler
def add_new_answer(cursor, message, question_id, username):
    date_time = datetime.now()
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message) 
                    VALUES (%(date_time)s, 0, %(question_id)s, %(message)s)
                    """,
                   {'date_time': date_time, 'question_id': question_id, 'message': message})
    last_answer_id = get_last_answer_id()
    user_id = data_handler_2.get_id_by_username(username)
    cursor.execute("""
                    INSERT INTO user_answer (answer_id, user_id)
                    VALUES (%(last_answer_id)s, %(user_id)s)
                    """,
                   {'last_answer_id': last_answer_id['last_value'], 'user_id': user_id['id']})

@database_common.connection_handler
def update_question(cursor, question_id, title, message, image):
    cursor.execute("""
                    UPDATE question
                    SET title = %(title)s,
                        message = %(message)s,
                        image = %(image)s
                    WHERE id = %(question_id)s;
                    """,
                   {'title': title, 'message': message, 'image': image, 'question_id': question_id})


@database_common.connection_handler
def update_answer(cursor, answer_id, message):
    cursor.execute("""
                UPDATE answer
                SET message = %(message)s
                WHERE id = %(answer_id)s
                AND id = %(answer_id)s;
                """,
                   {'answer_id': answer_id, 'message': message}
                   )


@database_common.connection_handler
def get_question_by_id(cursor, question_id):
    cursor.execute("""
                    SELECT * FROM question
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    question = cursor.fetchall()
    return question


@database_common.connection_handler
def get_answers_by_question_id(cursor, name):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE question_id = %(question_id)s
                    ORDER BY id ASC;
                    """,
                   {'question_id': name})
    answer_to_question = cursor.fetchall()
    return answer_to_question


@database_common.connection_handler
def update_view_number(cursor, view_number, name):
    cursor.execute("""
                    UPDATE question
                    SET view_number = %(view_number)s
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': name, 'view_number': view_number})


@database_common.connection_handler
def get_answer_by_id(cursor, answer_id):
    cursor.execute("""
                    SELECT * FROM answer
                    WHERE id = %(answer_id)s;
                    """,
                   {'answer_id': answer_id})
    answer = cursor.fetchone()
    return answer


@database_common.connection_handler
def update_answer_vote_number(cursor, answer_id, vote_number):
    cursor.execute("""
                    UPDATE answer
                    SET vote_number = %(vote_number)s
                    WHERE id = %(answer_id)s;
                    """,
                   {'answer_id': answer_id, 'vote_number': vote_number})


@database_common.connection_handler
def update_question(cursor, question_id, view_number, vote_number):
    cursor.execute("""
                    UPDATE question
                    SET view_number = %(view_number)s, vote_number = %(vote_number)s
                    WHERE id = %(question_id)s;
                    """,
                   {'question_id': question_id, 'view_number': view_number, 'vote_number': vote_number})


@database_common.connection_handler
def add_new_comment(cursor, message, question_id, username):
    date_time = datetime.now()
    cursor.execute("""
                    INSERT INTO comment (submission_time, message, question_id) 
                    VALUES (%(date_time)s, %(message)s, %(question_id)s)
                    """,
                   {'date_time': date_time, 'message': message, 'question_id': question_id})
    last_comment_id = get_last_comment_id()
    user_id = data_handler_2.get_id_by_username(username)
    cursor.execute("""
                    INSERT INTO user_comment (comment_id, user_id)
                    VALUES (%(last_comment_id)s, %(user_id)s)
                    """,
                   {'last_comment_id': last_comment_id['last_value'], 'user_id': user_id['id']})

@database_common.connection_handler
def get_all_comments(cursor, question_id):
    header = ['id', 'message', 'submission_time']
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE question_id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    comments = cursor.fetchall()
    rows = [
        [1, ]
    ]

    for dict_row in comments:
        rows.append([])
        for column_name in header:
            rows[len(rows) - 1].append(dict_row[column_name])
    return rows


@database_common.connection_handler
def delete_line(cursor, edit_id):
    cursor.execute("""
                    DELETE FROM comment 
                    WHERE id = %(edit_id)s;
                    """,
                   {'edit_id': edit_id})


@database_common.connection_handler
def get_all_comments_answer(cursor, answer_id):
    header = ['id', 'message', 'submission_time']
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE answer_id = %(answer_id)s;
                    """,
                   {'answer_id': answer_id})
    comments = cursor.fetchall()
    rows = [
        [1, ]
    ]

    for dict_row in comments:
        rows.append([])
        for column_name in header:
            rows[len(rows) - 1].append(dict_row[column_name])
    return rows


@database_common.connection_handler
def add_new_comment_answer(cursor, message, answer_id, username):
    date_time = datetime.now()
    cursor.execute("""
                    INSERT INTO comment (submission_time, message, answer_id) 
                    VALUES (%(date_time)s, %(message)s, %(answer_id)s)
                    """,
                   {'date_time': date_time, 'message': message, 'answer_id': answer_id})
    last_comment_id = get_last_comment_id()
    user_id = data_handler_2.get_id_by_username(username)
    cursor.execute("""
                    INSERT INTO user_comment (comment_id, user_id)
                    VALUES (%(last_comment_id)s, %(user_id)s)
                    """,
                   {'last_comment_id': last_comment_id['last_value'], 'user_id': user_id['id']})

@database_common.connection_handler
def get_tag(cursor, question_id):
    cursor.execute("""
                    SELECT tag_id FROM question_tag
                    WHERE question_id = %(question_id)s;
                    """,
                   {'question_id': question_id})
    tag_id = cursor.fetchone()['tag_id']
    cursor.execute("""
                    SELECT name FROM tag
                    WHERE id = %(tag_id)s;
                    """,
                   {'tag_id': tag_id})
    tag = cursor.fetchone()
    return tag


@database_common.connection_handler
def add_new_tag(cursor, new_tag):
    cursor.execute("""
                    INSERT INTO tag (name)
                    VALUES (%(new_tag)s);
                    """,
                   {'new_tag': new_tag})


@database_common.connection_handler
def get_search_results(cursor, search_phrase):
    cursor.execute("""
                    SELECT question.id, question.title, question.view_number, question.vote_number FROM question
                    JOIN answer ON question.id = answer.question_id
                    WHERE LOWER (title) LIKE %(search_phrase)s
                          OR LOWER (question.message) LIKE %(search_phrase)s
                          OR LOWER (answer.message) LIKE %(search_phrase)s
                    GROUP BY question.id
                    ORDER BY id;
                   """,
                   {'search_phrase': '%' + search_phrase.lower() + '%'})
    questions = cursor.fetchall()

    return questions


@database_common.connection_handler
def delete_tag(cursor, tag_id):
    cursor.execute("""
                    DELETE FROM question_tag
                    WHERE question_id = %(tag_id)s;
                    """,
                   {'tag_id': tag_id})


@database_common.connection_handler
def get_last_question_id(cursor):
    cursor.execute("""
                    SELECT last_value FROM question_id_seq;
                    """)
    last_question_id = cursor.fetchone()
    return last_question_id

@database_common.connection_handler
def get_last_answer_id(cursor):
    cursor.execute("""
                    SELECT last_value FROM answer_id_seq;
                    """)
    last_answer_id = cursor.fetchone()
    return last_answer_id

@database_common.connection_handler
def get_last_comment_id(cursor):
    cursor.execute("""
                    SELECT last_value FROM comment_id_seq;
                    """)
    last_comment_id = cursor.fetchone()
    return last_comment_id


@database_common.connection_handler
def get_last_tag_id(cursor):
    cursor.execute("""
                    SELECT last_value FROM tag_id_seq;
                    """)
    last_tag_id = cursor.fetchone()
    return last_tag_id


@database_common.connection_handler
def get_all_tags(cursor):
    cursor.execute("""
                    SELECT name FROM tag;
                    """)
    tags = cursor.fetchall()
    return tags


@database_common.connection_handler
def get_tag_id_by_tag_name(cursor, tag):
    cursor.execute("""
                    SELECT id FROM tag
                    WHERE name = %(tag)s;
                    """,
                   {'tag': tag})
    tag_id = cursor.fetchone()
    return tag_id


@database_common.connection_handler
def add_new_tag(cursor, new_tag):
    cursor.execute("""
                    SELECT name FROM tag
                    WHERE name = %(new_tag)s;
                    """,
                   {'new_tag': new_tag})
    tag_exist = cursor.fetchone()
    if not tag_exist:
        cursor.execute("""
                        INSERT INTO tag (name)
                        VALUES (%(new_tag)s);
                        """,
                       {'new_tag': new_tag})


@database_common.connection_handler
def delete_tag_from_question(cursor, question_id):
    cursor.execute("""
                    UPDATE question_tag
                    SET tag_id = 0
                    WHERE question_id = %(question_id)s;
                    """,
                   {'question_id': question_id})


@database_common.connection_handler
def get_selected_answers_by_question_id(cursor, id, answer_id):
    header = ['id', 'message']
    cursor.execute("""
                    SELECT id, message FROM comment
                    WHERE answer_id = %(answer_id)s
                    AND id = %(id)s;
                    """,
                   {'id': answer_id, 'answer_id': id})
    rows = cursor.fetchall()
    answer_rows = [

    ]

    for dict_row in rows:
        answer_rows.append([])
        for column_name in header:
            answer_rows[len(answer_rows) - 1].append(dict_row[column_name])
    return answer_rows


@database_common.connection_handler
def update_comment(cursor, id, message):
    cursor.execute("""
                    UPDATE comment
                    SET message = %(message)s
                    WHERE id = %(id)s;
                    """,
                   {'message': message, 'id': id})


@database_common.connection_handler
def get_question_id_by_answer_id(cursor, answer_id):
    cursor.execute("""
                    SELECT question_id FROM answer
                    WHERE id = %(answer_id)s;
                    """,
                   {'answer_id': answer_id})
    question_id = cursor.fetchone()
    return question_id


@database_common.connection_handler
def get_comment_by_id(cursor, comment_id):
    cursor.execute("""
                    SELECT * FROM comment
                    WHERE id = %(comment_id)s;
                    """,
                   {'comment_id': comment_id})
    comment_id = cursor.fetchone()
    return comment_id

@database_common.connection_handler
def count_tags(cursor):
    cursor.execute("""
                    SELECT name, count(question_id)
                    FROM tag
                    JOIN question_tag ON id = tag_id
                    WHERE name IS NOT NULL
                    GROUP BY name;
                    """)
    tags = cursor.fetchall()
    return tags

