from ext import app
from routes.basket import basket_bp
from routes.payments import payment_bp

app.register_blueprint(basket_bp)
app.register_blueprint(payment_bp)
