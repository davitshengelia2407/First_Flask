from ext import app, db
from routes import *


if __name__ == "__main__":
    app.run("0.0.0.0", port=5000)
