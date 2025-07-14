from ext import app, db
from routes import *

from flask_migrate import upgrade

if __name__ == "__main__":
    with app.app_context():
        upgrade()  # Applies migrations on startup (Render-safe fallback)

    app.run("0.0.0.0", port=5000)
