import csv
def get_all_user_story():
    with open("questions.csv", 'r') as file:
        csv_file = csv.reader(file)
        table = [item for item in csv_file]
    return table


def get_all_answer_story():
    with open("answers.csv", 'r') as file:
        answer_csv = csv.reader(file)
        answer_table = [item for item in answer_csv]
    return answer_table


def get_answers_by_question_id(id):
    table = get_all_answer_story()
    answers_for_question = []
    for answers in table:
        if answers[0] == str(id):
            answers_for_question.append(answers)
    return answers_for_question


def save_routine(table):
    with open("questions.csv", 'a') as file:
        csv_file = csv.writer(file)
        csv_file.writerow(table)
    return table


def generate_id():
    ids = get_ids()
    if len(ids) == 0:
        return 1
    else:
        return max(ids) + 1


def get_ids():
    table = get_all_user_story()
    ids = []
    for rows in table:
        ids.append(int(rows[0]))
    return int(ids[-1])+1


def update_csv_info(newdata,name):
    table = get_all_user_story()
    for row in table:
        row_number = table.index(row)
        if int(row[0]) == int(name):
            table[row_number][3] = str(newdata)
            return view_number(table)


def view_number(counter_num):
    with open("questions.csv", 'w') as file:
        csv_file = csv.writer(file, delimiter=',', quotechar='\"')
        for row in counter_num:
            csv_file.writerow(row)


def update_csv_info_pop(newdata,name):
    table = get_all_user_story()
    for row in table:
        row_number = table.index(row)
        if int(row[0]) == int(name):
            table[row_number][4] = str(newdata)
            return view_number(table)


def get_answers_by_question_id(id):
    table = get_all_answer_story()
    answers_for_question = []
    for answers in table:
        if answers[0] == str(id):
            answers_for_question.append(answers)
    return answers_for_question


def get_all_answer_story():
    with open("answers.csv", 'r') as file:
        answer_csv = csv.reader(file)
        answer_table = [item for item in answer_csv]
    return answer_table


def save_routine_to_answer(table):
    with open("answers.csv", 'a') as file:
        csv_file = csv.writer(file)
        csv_file.writerow(table)
    return table


def get_ids_ans():
    table = get_all_answer_story()
    ids = []
    for rows in table:
        ids.append(int(rows[1]))
    return int(ids[-1])+1


def update_csv_answer_pop(newdata, name, question_id):
    table = get_all_answer_story()
    for row in table:
        row_number = table.index(row)
        if int(row[0]) == int(name) and int(row[1]) == int(question_id):
            table[row_number][3] = str(newdata)
            return view_number_answer(table)


def view_number_answer(counter_num):
    with open("answers.csv", 'w') as file:
        csv_file = csv.writer(file, delimiter=',', quotechar='\"')
        for row in counter_num:
            csv_file.writerow(row)


def get_selected_answers_by_question_id(id, id_2):
    table = get_all_answer_story()
    answer_for_the_question = []
    for answers in table:
        if answers[0] == str(id) and answers[1] == str(id_2):
            answer_for_the_question.append(answers)
    print(answer_for_the_question)
    return answer_for_the_question


