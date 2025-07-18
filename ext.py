from flask import Flask, request
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from flask_babel import Babel
from flask_migrate import Migrate

app = Flask(__name__)
app.config["SECRET_KEY"] = "daculisaiti"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///flask-sqlite.db"
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
app.config['BABEL_SUPPORTED_LOCALES'] = ['en', 'ka']

db = SQLAlchemy(app)
login_manager = LoginManager(app)
migrate = Migrate(app, db)

def get_locale():
    return request.args.get('lang') or request.accept_languages.best_match(['en', 'ka'])

babel = Babel(app, locale_selector=get_locale)

login_manager.login_view = 'sign_in'

@app.context_processor
def inject_basket_count():
    if current_user.is_authenticated:
        from models import Basket
        basket = Basket.query.filter_by(user_id=current_user.id).first()
        count = sum(item.quantity for item in basket.items) if basket else 0
        return dict(basket_count=count)
    return dict(basket_count=0)

