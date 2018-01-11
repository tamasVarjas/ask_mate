from flask import Flask, request, render_template, redirect, url_for
import data_handler

app = Flask(__name__)


@app.route('/')
def index():
    info = data_handler.get_all_data('question')
    return render_template("main_page.html", info=info)


@app.route('/question/add_new_question', methods=['GET', 'POST'])
def add_new_question():
    if request.method == 'GET':
        tags = data_handler.get_all_tags()
        return render_template("new_question.html", tags = tags)
    else:
        title = request.form["title"]
        message = request.form["message"]
        image = request.form["image"]
        tag = request.form["tag"]
        data_handler.add_new_question(title, message, image, tag)
        return redirect("/")


@app.route('/question/<int:name>', methods=["GET", "POST"])
def counter_plus(name):
    info = data_handler.get_question_by_id(name)
    info_tag = data_handler.get_tag(name)
    question_data = info[0]['title']
    detail_data = info[0]['message']
    picture_data = info[0]['image']
    view_number = info[0]['view_number']
    popular_number = info[0]['vote_number']
    tag = info_tag['name']
    answers = data_handler.get_answers_by_question_id(name)
    if request.method == 'GET':
        view_number += 1
        info[0]['view_number'] = view_number
        data_handler.update_view_number(view_number, name)
    return render_template("question.html", name=name, question_data=question_data, detail_data=detail_data,
                           picture_data=picture_data, view_number=view_number, popular_number=popular_number,
                           tag=tag, answers=answers)


@app.route('/like/<int:name>', methods=["GET"])
def popularity(name):
    question = data_handler.get_question_by_id(name)
    popular_number = question[0]['vote_number']
    view_number = question[0]['view_number']
    if request.method == 'GET':
        popular_number += 1
        view_number -= 1
        data_handler.update_question(name, view_number, popular_number)
    return redirect(url_for('counter_plus', name=name))


@app.route('/dislike/<int:name>', methods=["GET"])
def not_so_popular(name):
    question = data_handler.get_question_by_id(name)
    popular_number = question[0]['vote_number']
    view_number = question[0]['view_number']
    if request.method == 'GET':
        popular_number += -1
        view_number -= 1
        data_handler.update_question(name, view_number, popular_number)
    return redirect(url_for('counter_plus', name=name))


@app.route("/question/add_new_answer/<int:name>", methods=['GET', 'POST'])
def new_question(name):
    answer = request.form["answer"]
    data_handler.add_new_answer(answer, name)
    return redirect(url_for('counter_plus', name=name))


@app.route('/answer_like/<int:name>/<int:question_id>', methods=["GET", "POST"])
def answer_less_popularity(name, question_id):
    answer = data_handler.get_answer_by_id(name)
    answer_popular_number = answer[0]['vote_number']
    if request.method == 'GET':
        answer_popular_number += 1
        data_handler.update_answer_vote_number(name, answer_popular_number)
    return redirect(
        url_for('counter_plus', answer_popular_number=answer_popular_number, name=name, question_id=question_id))


@app.route('/answer_dislike/<int:name>/<int:question_id>', methods=["GET", "POST"])
def answer_popularity(name, question_id):
    answer = data_handler.get_answer_by_id(name)
    answer_popular_number = answer[0]['vote_number']
    if request.method == 'GET':
        answer_popular_number -= 1
        data_handler.update_answer_vote_number(name, answer_popular_number)
    return redirect(
        url_for('counter_plus', answer_popular_number=answer_popular_number, name=name, question_id=question_id))


@app.route('/answer_edit/<int:name>/<int:question_id>', methods=["GET", "POST"])
def answer_edit(name, question_id):
    if request.method == 'GET':
        edit_selected = data_handler.get_selected_answers_by_question_id(name, question_id)
        return render_template("answer_edit.html", selected_answer=edit_selected)
    # else:
    # new_answer=request.form['edit_answer']
    # !!!!! data_handler.change_answer(name, question_id, new_answer)
    # return redirect (url_for('/question/<int:name>'))


@app.route('/comment/<int:name>', methods=["GET", "POST"])
def comment(name):
    if request.method == 'GET':
        comments = data_handler.get_all_comments(name)
        return render_template("comment.html", name=name, comments=comments)
    else:
        comment = request.form["comment"]
        data_handler.add_new_comment(comment, name)
        comments = data_handler.get_all_comments(name)
        return render_template("comment.html", name=name, comments=comments)


@app.route('/comment_answer/<int:name>', methods=["GET", "POST"])
def comment_answer(name):
    if request.method == 'GET':
        comments = data_handler.get_all_comments_answer(name)
        return render_template("comment_answer.html", name=name, comments=comments)
    else:
        comment_answer = request.form["comment"]
        data_handler.add_new_comment_answer(comment_answer, name)
        comments = data_handler.get_all_comments_answer(name)
        return render_template("comment_answer.html", name=name, comments=comments)


@app.route('/search_results', methods=['GET', 'POST'])
def find_search_results():
    form_data = request.form.to_dict()
    search_phrase = form_data['search_phrase']

    return redirect(url_for('show_search_results', search_phrase=search_phrase))


@app.route('/search?q=<search_phrase>')
def show_search_results(search_phrase):
    results = data_handler.get_search_results(search_phrase)
    return render_template('search_results.html', results=results)


@app.route('/delete-tag/<int:name>')
def delete_tag_from_question(name):
    data_handler.delete_tag_from_question(name)
    return redirect(url_for('counter_plus', name=name))

@app.route('/delete_comment/<int:name>/<int:question_id>')
def delete_comment(name, question_id):
    data_handler.delete_line(question_id)
    comments = data_handler.get_all_comments(name)
    print(comments)
    return render_template('comment.html', name=name, comments=comments)


@app.route('/delete_comment_answer/<int:name>/<int:question_id>')
def delete_comment_answer(name, question_id):
    data_handler.delete_line(question_id)
    comments = data_handler.get_all_comments_answer(name)
    return render_template('comment_answer.html', name=name, comments=comments)


@app.route('/answer_edit_comment/<int:name>/<int:question_id>', methods=["GET", "POST"])
def answer_edit_comment(name, question_id):
    if request.method == 'GET':
        edit_selected = data_handler.get_selected_answers_by_question_id(name, question_id)
        return render_template("answer_edit.html", selected_answer=edit_selected, question_id=question_id)
    else:
        new_answer=request.form['message']
        data_handler.update_answer(name, question_id, new_answer)
        return redirect (url_for('/question/<int:name>'))


if __name__ == '__main__':
    app.run(debug=True)
