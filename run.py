# from ext import app, db
# from  routes.basket import *
# from routes import *
# from routes.basket import basket_bp
#
# app.register_blueprint(basket_bp)
#
# if __name__ == "__main__":
#     app.run("0.0.0.0", port=5000)

from ext import app, db
from routes.basket import basket_bp
from routes import routes  # this runs your @app.route decorators

app.register_blueprint(basket_bp)

if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)
