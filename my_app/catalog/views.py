from flask import render_template, request, url_for, Blueprint

home  = Blueprint('home',__name__)

@home.route('/')
def index():
    # Index page logic goes here
    return render_template('index.html')