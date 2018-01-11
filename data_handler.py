from datetime import datetime
import time
import database_common


def timestamp_to_datetime(database):
    for data in database:
        data['submission_time'] = datetime.datetime.fromtimestamp(int(data['submission_time'])).strftime(
            '%Y-%m-%d %H:%M:%S')

    return database


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


# TODO: It's not the best that it makes timestamp_to_datetime, but at this moment, this one is working.
def edit_data(database, updated_data, _id):
    for data in database:
        if _id == data['id']:
            for element in updated_data:
                data[element] = updated_data[element]

    return database


def make_unix_timestamp():
    return round(time.time())


@database_common.connection_handler
def add_new_question(cursor, title, message, image, tag):
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
    cursor.execute("""
                    INSERT INTO question_tag (question_id, tag_id) 
                    VALUES (%(last_question_id)s, %(tag_id)s);
                    """,
                   {'last_question_id': last_question_id['last_value'], 'tag_id': tag_id['id']})

@database_common.connection_handler
def add_new_answer(cursor, message, question_id):
    date_time = datetime.now()
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message) 
                    VALUES (%(date_time)s, 0, %(question_id)s, %(message)s)
                    """,
                   {'date_time': date_time, 'question_id': question_id, 'message': message})


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
def update_answer(cursor, name, question_id, message):
    cursor.execute("""
                UPDATE answer
                SET message = %(message)s,
                WHERE id = %(question_id)s;
                AND id = %(id);
                """,
                   {'id': name, 'question_id': question_id, 'message': message})



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
                    WHERE question_id = %(question_id)s;
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
    answer = cursor.fetchall()
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
def add_new_comment(cursor, message, question_id):
    date_time = datetime.now()
    cursor.execute("""
                    INSERT INTO comment (submission_time, message, question_id) 
                    VALUES (%(date_time)s, %(message)s, %(question_id)s)
                    """,
                   {'date_time': date_time, 'message': message, 'question_id': question_id})


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
                    DELETE from comment 
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
    print(rows)
    return rows


@database_common.connection_handler
def add_new_comment_answer(cursor, message, answer_id):
    date_time = datetime.now()
    cursor.execute("""
                    INSERT INTO comment (submission_time, message, answer_id) 
                    VALUES (%(date_time)s, %(message)s, %(answer_id)s)
                    """,
                   {'date_time': date_time, 'message': message, 'answer_id': answer_id})


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
                    SELECT id, title, view_number, vote_number FROM question
                    WHERE title LIKE %(search_phrase)s OR message LIKE %(search_phrase)s
                    ORDER BY id;
                   """,
                   {'search_phrase': '%' + search_phrase + '%'})
    questions = cursor.fetchall()

    return questions


@database_common.connection_handler
def delete_tag(cursor, tag_id):
    cursor.execute("""
                    DELETE FROM tag
                    WHERE id = %(tag_id)s;
                    """,
                   {'tag_id': tag_id})

@database_common.connection_handler
def get_last_question_id(cursor):
    cursor.execute("""
                    SELECT last_value FROM question_id_seq;
                    """)
    last_question_id = cursor.fetchone()
    print(last_question_id['last_value'])
    return last_question_id

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
def get_selected_answers_by_question_id(cursor, id, question_id):
    header = ['id', 'message']
    cursor.execute("""
                    SELECT id, message FROM answer
                    WHERE question_id = %(question_id)s
                    AND id = %(id)s;
                    """,
                   {'question_id': question_id, 'id': id})
    rows = cursor.fetchall()
    answer_rows = [
        [1, ]
    ]

    for dict_row in rows:
        answer_rows.append([])
        for column_name in header:
            answer_rows[len(answer_rows) - 1].append(dict_row[column_name])
    print(answer_rows)
    return answer_rows

