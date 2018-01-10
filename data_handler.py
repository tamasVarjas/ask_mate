import datetime
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
                    SELECT * FROM """ + data_table + """;
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


def remove_answers_by_question(question_id):
    answers = connection.get_data_from_file(connection.ANSWER_FILE_PATH)
    for answer in answers:
        if answer['question_id'] == str(question_id):
            answers.remove(answer)

    return answers


def make_new_id(database):
    ids = []
    for data in database:
        ids.append(int(data['id']))

    return str(max(ids) + 1)


def make_unix_timestamp():
    return round(time.time())


def append_database(database, new_data):
    new_data['id'] = make_new_id(database)
    new_data['submission_time'] = make_unix_timestamp()
    database.append(new_data)
    return database


# TODO: It's not the best that it makes timestamp_to_datetime, but at this moment, this one is working.
def get_question_by_id(question_id):
    for data in timestamp_to_datetime(connection.get_data_from_file(connection.QUESTION_FILE_PATH)):
        if question_id == data['id']:
            return data


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


print(delete_answer(2))


@database_common.connection_handler
def get_search_results(cursor, phrase):
    cursor.execute("""
                    SELECT question_id FROM answer
                    WHERE message LIKE %(search_phrase)s;
                    """,
                   {'search_phrase': '%' + phrase + '%'})
    question_id_list = cursor.fetchall()

    cursor.execute("""
                    SELECT * FROM question
                    WHERE title LIKE %(search_phrase)s OR message LIKE %(search_phrase)s;
                   """,
                   {'search_phrase': '%' + phrase + '%'})
    if len(question_id_list) >= 1:
        for question_id in question_id_list:
            cursor.execute("""
                                SELECT * FROM question
                                WHERE id = %(id)s;
                               """,
                           {'id': question_id})
    results = cursor.fetchall()

    return results
