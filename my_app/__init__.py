from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from my_app.catalog.views import home

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # SQLite kullanımı, başka bir veritabanı kullanabilirsiniz
db = SQLAlchemy(app)
app.register_blueprint(home)

app.app_context().push()
db.create_all()