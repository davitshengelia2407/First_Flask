# from ext import app
# from routes.basket import basket_bp
# from routes.payments import payment_bp
# from  .routes import routes
#
# app.register_blueprint(basket_bp)
# app.register_blueprint(payment_bp)

from .routes import routes
from .basket import basket_bp
from .payments import payment_bp
