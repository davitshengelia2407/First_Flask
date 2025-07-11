from flask import Flask, request
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SECRET_KEY"] = "daculisaiti"
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'ka']
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask-sqlite.db"
login_manager = LoginManager(app)


db = SQLAlchemy(app)

def get_locale():
    return request.args.get('lang') or request.accept_languages.best_match(['en', 'ka'])

babel = Babel(app, locale_selector=get_locale)

migrate = Migrate(app, db)

login_manager.login_view = 'sign_in'


