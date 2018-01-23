from flask import Flask, request, render_template, redirect, url_for
import data_handler

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("main_page.html")


@app.route('/table')
def table():
    info = data_handler.get_all_data('question')
    return render_template("table.html", info=info)


@app.route('/question/add_new_question', methods=['GET', 'POST'])
def add_new_question():
    if request.method == 'GET':
        tags = data_handler.get_all_tags()
        return render_template("new_question.html", tags=tags)
    else:
        title = request.form["title"]
        message = request.form["message"]
        image = request.form["image"]
        tag = request.form["tag"]
        data_handler.add_new_question(title, message, image, tag)
        return redirect("/")


@app.route('/question/<int:question_id>', methods=["GET", "POST"])
def question_details(question_id):
    info = data_handler.get_question_by_id(question_id)
    info_tag = data_handler.get_tag(question_id)
    question_data = info[0]['title']
    detail_data = info[0]['message']
    picture_data = info[0]['image']
    view_number = info[0]['view_number']
    popular_number = info[0]['vote_number']
    tag = info_tag['name']
    answers = data_handler.get_answers_by_question_id(question_id)
    if request.method == 'GET':
        view_number += 1
        info[0]['view_number'] = view_number
        data_handler.update_view_number(view_number, question_id)
    return render_template("question.html", question_id=question_id, question_data=question_data,
                           detail_data=detail_data,
                           picture_data=picture_data, view_number=view_number, popular_number=popular_number,
                           tag=tag, answers=answers)


@app.route('/like/<int:question_id>', methods=["GET"])
def popularity(question_id):
    question = data_handler.get_question_by_id(question_id)
    popular_number = question[0]['vote_number']
    view_number = question[0]['view_number']
    if request.method == 'GET':
        popular_number += 1
        view_number -= 1
        data_handler.update_question(question_id, view_number, popular_number)
    return redirect(url_for('question_details', question_id=question_id))


@app.route('/dislike/<int:question_id>', methods=["GET"])
def not_so_popular(question_id):
    question = data_handler.get_question_by_id(question_id)
    popular_number = question[0]['vote_number']
    view_number = question[0]['view_number']
    if request.method == 'GET':
        popular_number += -1
        view_number -= 1
        data_handler.update_question(question_id, view_number, popular_number)
    return redirect(url_for('question_details', question_id=question_id))


@app.route("/question/add_new_answer/<int:question_id>", methods=['GET', 'POST'])
def add_new_answer(question_id):
    answer = request.form["answer"]
    data_handler.add_new_answer(answer, question_id)
    return redirect(url_for('question_details', question_id=question_id))


@app.route('/answer_like/<int:question_id>/<int:answer_id>', methods=["GET", "POST"])
def answer_more_popularity(question_id, answer_id):
    answer = data_handler.get_answer_by_id(answer_id)
    answer_popular_number = answer['vote_number']
    question = data_handler.get_question_by_id(question_id)
    view_number = question[0]['view_number']
    popular_number = question[0]['vote_number']
    if request.method == 'GET':
        answer_popular_number += 1
        data_handler.update_answer_vote_number(answer_id, answer_popular_number)
        view_number -= 1
        data_handler.update_question(question_id, view_number, popular_number)
    return redirect(
        url_for('question_details', question_id=question_id))


@app.route('/answer_dislike/<int:question_id>/<int:answer_id>', methods=["GET", "POST"])
def answer_less_popularity(question_id, answer_id):
    answer = data_handler.get_answer_by_id(answer_id)
    answer_popular_number = answer['vote_number']
    question = data_handler.get_question_by_id(question_id)
    view_number = question[0]['view_number']
    popular_number = question[0]['vote_number']
    if request.method == 'GET':
        answer_popular_number -= 1
        data_handler.update_answer_vote_number(answer_id, answer_popular_number)
        view_number -= 1
        data_handler.update_question(question_id, view_number, popular_number)
    return redirect(
        url_for('question_details', question_id=question_id))


@app.route('/answer_edit/<int:question_id>/<int:answer_id>', methods=["GET", "POST"])
def answer_edit(question_id, answer_id):
    if request.method == 'GET':
        answer = data_handler.get_answer_by_id(answer_id)
        return render_template("answer_edit.html", answer=answer)

    message = request.form['message']
    data_handler.update_answer(answer_id, message)
    return redirect(url_for('question_details', question_id=question_id))


@app.route('/comment/<int:question_id>', methods=["GET", "POST"])
def question_comment(question_id):
    if request.method == 'GET':
        comments = data_handler.get_all_comments(question_id)
        return render_template("comment.html", question_id=question_id, comments=comments)
    else:
        comment = request.form["comment"]
        data_handler.add_new_comment(comment, question_id)
        comments = data_handler.get_all_comments(question_id)
        return render_template("comment.html", question_id=question_id, comments=comments)


@app.route('/comment_answer/<int:answer_id>', methods=["GET", "POST"])
def answer_comment(answer_id):
    if request.method == 'GET':
        comments = data_handler.get_all_comments_answer(answer_id)
        question_id = data_handler.get_question_id_by_answer_id(answer_id)
        return render_template("comment_answer.html", answer_id=answer_id, comments=comments, question_id=question_id)
    else:
        comment_answer = request.form["comment"]
        data_handler.add_new_comment_answer(comment_answer, answer_id)
        comments = data_handler.get_all_comments_answer(answer_id)
        question_id = data_handler.get_question_id_by_answer_id(answer_id)
        return render_template("comment_answer.html", answer_id=answer_id, comments=comments, question_id=question_id)


@app.route('/search_results', methods=['GET', 'POST'])
def find_search_results():
    form_data = request.form.to_dict()
    search_phrase = form_data['search_phrase']

    return redirect(url_for('show_search_results', search_phrase=search_phrase))


@app.route('/search?q=<search_phrase>')
def show_search_results(search_phrase):
    results = data_handler.get_search_results(search_phrase)
    return render_template('search_results.html', results=results)


@app.route('/delete-tag/<int:question_id>')
def delete_tag_from_question(question_id):
    data_handler.delete_tag_from_question(question_id)
    return redirect(url_for('question_details', question_id=question_id))


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


@app.route('/edit_comment_answer/<int:answer_id>/<int:comment_id>', methods=["GET", "POST"])
def answer_edit_comment(answer_id, comment_id):
    comment = data_handler.get_comment_by_id(comment_id)
    if request.method == 'GET':
        return render_template("comment_edit.html", comment=comment, answer_id=answer_id)
    else:
        message = request.form['message']
        comment_id = comment['id']
        data_handler.update_comment(comment_id, message)
        return redirect(url_for('comment_answer', name=answer_id))


if __name__ == '__main__':
    app.run(debug=True)
