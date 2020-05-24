from flask import Flask, request, render_template, redirect, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *


app = Flask(__name__)
app.config['SECRET_KEY'] = "Secret-Key"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
RESPONSE_KEY = "responses"

debug = DebugToolbarExtension(app)

satisfaction_survey = surveys['satisfaction']
title = satisfaction_survey.title

@app.route('/')
def home_page():
    return render_template('survey.html', title=title, instructions= satisfaction_survey.instructions)

@app.route("/start", methods=["POST"])
def start_questionair():
    session[RESPONSE_KEY] = []

    return redirect("/question/0")

@app.route("/question/<int:index>")
def question_page(index):
    """Checks for the a valid question then redirects for /thank-you or next question

    :param index: index of the current question
    :return: redirects to the next page
    """
    responses = session[RESPONSE_KEY]

    try:
        question = satisfaction_survey.questions[index].question
        choices = satisfaction_survey.questions[index].choices
    except IndexError:
        return redirect('/thank-you')

    if (len(responses) != index):
        return redirect(f"/question/{len(responses)}")

    return render_template('question.html', title=title, question=question, index=index, choices=choices)

@app.route("/question/<int:index>", methods=["POST"])
def handle_answers(index):
    """handles the answers passed with the post request and pushes to the next question"""
    choice = request.form["answer"]

    responses = session[RESPONSE_KEY]
    responses.append(choice)
    session[RESPONSE_KEY] = responses

    return redirect(f"/question/{len(responses)}")



@app.route('/thank-you')
def finish_page():
    return render_template("finished.html", title=title)