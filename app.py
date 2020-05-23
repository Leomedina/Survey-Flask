from flask import Flask, request, render_template
from flask_debugtoolbar import DebugToolbarExtension
from surveys import *

app = Flask(__name__)
app.config['SECRET_KEY'] = "Secret-Key"
debug = DebugToolbarExtension(app)

responses = []
satisfaction_survey = surveys['satisfaction']

@app.route('/')
def home_page():
    
    return render_template('survey.html', title=satisfaction_survey.title)

