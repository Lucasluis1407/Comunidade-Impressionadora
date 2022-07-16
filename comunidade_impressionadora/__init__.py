from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail, Message


app = Flask(__name__)

app.config['SECRET_KEY'] = '1c4480dd660f7a363fa6b77c48e68344'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'lucasluisouza@gmail.com'
app.config['MAIL_PASSWORD'] = 'tmsdmqpgfydugaqv'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
loginManager = LoginManager(app)
mail = Mail(app)


loginManager.login_view = 'login'
loginManager.login_message = 'Por favor faça Login para acessar esta página'
loginManager.login_message_category = 'alert-info'

from comunidade_impressionadora import routes