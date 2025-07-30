
from ext import app, db
from routes.basket import basket_bp
from routes import routes

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)
