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
                    WHERE id = %(question_id)s;
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


#@app.route('/edit_comment_answer/<int:edit_id>', methods=['GET', 'POST'])
#def edit_comment_answer(edit_id):
    #if request.method=='GET':
        #edit_selected_answer = data_handler.selected_comment_answer_to_edit(edit_id)
        #return render_template("/edit.html", selected_applicant=edit_selected)
    #else:
        #new_number=request.form['new_phone']
        #data_manager.change_phone(edit_id, new_number)
        #applicants=data_manager.get_all_applicants()
        #return render_template("/applicant_with_all_data", applicants=applicants)


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

