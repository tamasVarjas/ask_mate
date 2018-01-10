from flask import Flask, request, render_template, redirect, url_for
import data_handler

app = Flask(__name__)

@app.route('/')
def index():
    info=data_handler.get_all_user_story()
    return render_template("main_page.html",info=info)


@app.route('/question/add_new_question', methods=['GET','POST'])
def add_new_question():
    if request.method=='GET':
        return render_template("new_question.html")
    else:
        title = request.form["title"]
        more_detail = request.form["more_detail"]
        picture_link = request.form["pic_link"]
        id = data_handler.get_ids()
        view_number=0
        popular_number=0
        story_elements = [id, title, more_detail,view_number,popular_number, picture_link]
        data_handler.save_routine(story_elements)
        return redirect("/")


@app.route('/question/<int:name>', methods=["GET", "POST"])
def counter_plus(name):
    info=data_handler.get_all_user_story()
    question_data=info[name-1][1]
    detail_data=info[name-1][2]
    picture_data=info[name-1][5]
    view_number=int(info[name-1][3])
    popular_number=int(info[name-1][4])
    answers=data_handler.get_answers_by_question_id(name)
    if request.method == 'GET':
        view_number += 1
        info[name-1][3] = view_number
        data_handler.update_csv_info(view_number,name)
    return render_template("question.html",name=name,question_data=question_data,detail_data=detail_data,picture_data=picture_data,view_number=view_number,popular_number=popular_number,answers=answers)


@app.route('/like/<int:name>',methods=["GET"])
def popularity(name):
    info = data_handler.get_all_user_story()
    popular_number=int(info[name-1][4])
    view_number=int(info[name-1][3])
    if request.method == 'GET':
        popular_number += 1
        view_number -= 1
        data_handler.update_csv_info_pop(popular_number,name)
        data_handler.update_csv_info(view_number,name)
    return redirect (url_for('counter_plus', name=name))


@app.route('/dislike/<int:name>',methods=["GET"])
def not_so_popular(name):
    info = data_handler.get_all_user_story()
    popular_number=int(info[name-1][4])
    view_number=int(info[name-1][3])
    if request.method == 'GET':
        popular_number += -1
        view_number -= 1
        data_handler.update_csv_info_pop(popular_number,name)
        data_handler.update_csv_info(view_number,name)
    return redirect (url_for('counter_plus', name=name))


@app.route("/question/add_new_answer/<int:name>",methods=['GET','POST'])
def new_question(name):
    answer = request.form["answer"]
    id_answer = data_handler.get_ids_ans()
    popularity = 0
    answer_elements = [name, id_answer, answer,popularity]
    data_handler.save_routine_to_answer(answer_elements)
    return redirect (url_for('counter_plus', name=name))


@app.route('/answer_like/<int:name>/<int:question_id>',methods=["GET","POST"])
def answer_less_popularity(name,question_id):
    info = data_handler.get_all_answer_story()
    answer_popular_number=int(info[question_id-1][3])
    if request.method == 'GET':
        answer_popular_number += 1
        data_handler.update_csv_answer_pop(answer_popular_number,name,question_id)
    return redirect (url_for('counter_plus', answer_popular_number=answer_popular_number, name=name, question_id=question_id))


@app.route('/answer_dislike/<int:name>/<int:question_id>',methods=["GET","POST"])
def answer_popularity(name,question_id):
    info = data_handler.get_all_answer_story()
    answer_popular_number=int(info[question_id-1][3])
    if request.method == 'GET':
        answer_popular_number -= 1
        data_handler.update_csv_answer_pop(answer_popular_number,name,question_id)
    return redirect (url_for('counter_plus', answer_popular_number=answer_popular_number, name=name, question_id=question_id))


@app.route('/answer_edit/<int:name>/<int:question_id>', methods=["GET", "POST"])
def answer_edit(name, question_id):
    if request.method=='GET':
        edit_selected = data_handler.get_selected_answers_by_question_id(name, question_id)
        return render_template("answer_edit.html", selected_answer=edit_selected)
    else:
        new_answer=request.form['new_answer']
        data_handler.change_answer(edit_id, new_number)
        applicants=data_manager.get_all_applicants()
        return render_template("/applicant_with_all_data", applicants=applicants)
    return render_template ("answer_edit.html")


if __name__ == '__main__':
    app.run(debug=True)




