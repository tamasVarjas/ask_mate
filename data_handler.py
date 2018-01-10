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
                    SELECT submission_time FROM """ + data_table + """;
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


def get_answer_by_id(answer_id):
    answers = connection.get_data_from_file(connection.ANSWER_FILE_PATH)
    for answer in answers:
        if answer['id'] == answer_id:
            return answer


def make_unix_timestamp():
    return round(time.time())


@database_common.connection_handler
def add_new_question(cursor, title, message, image):
    date_time = datetime.now()
    cursor.execute("""
                    INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
                    VALUES (%(date_time)s, 0, 0, %(title)s, %(message)s, %(image)s); 
                    """,
                   {'date_time': date_time, 'title': title, 'message': message, 'image': image})

@database_common.connection_handler
def add_new_answer(cursor, message, image, question_id):
    date_time = datetime.now()
    cursor.execute("""
                    INSERT INTO answer (submission_time, vote_number, question_id, message, image) 
                    VALUES (%(date_time)s, 0, %(question_id)s, %(message)s, %(image)s)
                    """,
                   {'date_time': date_time, 'question_id': question_id, 'message': message, 'image': image})

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
def update_answer(cursor, message, image):
    pass

update_question(4, 'Cím', 'Kabbe!', 'valami kép')
add_new_answer('Valami üzenet', 'valami kép', 3)