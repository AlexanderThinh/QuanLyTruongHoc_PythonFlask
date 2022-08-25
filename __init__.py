
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_babelex import Babel
from flask_login import LoginManager

app = Flask(__name__)
app.secret_key = '#$%dsds#$gdfaslk^&@swednskfia'

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:themilkyway@localhost/quanlyhocsinh?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db =SQLAlchemy(app=app)
babel = Babel(app=app)
login = LoginManager(app=app)

@babel.localeselector
def get_locale():
        return 'vi'