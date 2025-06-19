from flask import Flask, render_template

app = Flask(__name__)


profiles = [
    {"name": "davit",  "surname": "shengelia", "image_URL": "skami.jpg"},
    {"name": "anna",  "surname": "iarajuli", "image_URL": "magida.png"},
    {"name": "anna",  "surname": "grdzelishvili", "image_URL": "plates.webp"},
]

capitals = [
    {
        "id": 1,
        "name": "New York",
        "image": "newyork.webp",
        "description": "Bustling U.S. metropolis, famed for skyscrapers, Times Square, and cultural diversity."
    },
    {
        "id": 2,
        "name": "Tbilisi",
        "image": "tbilisi.jpeg",
        "description": "Georgia's vibrant capital, blends historic charm with modern life, nestled along the Mtkvari River."
    },
    {
        "id": 3,
        "name": "Kyiv",
        "image": "kiew.jpeg",
        "description": "Ukraine's historic capital, rich in golden-domed churches, Soviet legacy, and Dnipro River views."
    },
    {
        "id": 4,
        "name": "London",
        "image": "london.jpeg",
        "description": "UK's vibrant capital, home to Big Ben, Buckingham Palace, and a global finance, culture hub."
    },
    {
        "id": 5,
        "name": "Prague",
        "image": "prague.jpeg",
        "description": "Czech gem, boasts Gothic castles, Charles Bridge, and a fairytale Old Town by the Vltava."
    },
    {
        "id": 6,
        "name": "Reykjavik",
        "image": "iceland.png",
        "description": "Iceland's cozy capital, offers Nordic charm, hot springs, and Northern Lights views."
    },
    {
        "id": 7,
        "name": "Rome",
        "image": "rome.jpeg",
        "description": "Italy's eternal city, with Colosseum, Roman Forum, and Vatican’s art and history marvels."
    },
    {
        "id": 8,
        "name": "Bern",
        "image": "bern.webp",
        "description": "Swiss capital, blends medieval charm, Aare River beauty, and the iconic Bear Pit park."
    }
]

footer_icons = [
    {"name": "Twitter", "filename": "twitter.png"},
    {"name": "Telegram", "filename": "telegram.png"},
    {"name": "Instagram", "filename": "instagram.png"},
    {"name": "GitHub", "filename": "github.png"}
]

role = "user"

@app.context_processor
def inject_footer_icons():
    return dict(footer_icons=footer_icons)

@app.route("/")
def home():
    return render_template("index.html", country_capitals = capitals)

@app.route("/<int:trip_id>")
def trips(trip_id):
    return  render_template("trip.html", trip=capitals[trip_id - 1], role = role)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/sign-up")
@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/log-in")
@app.route("/sign-in")
def sign_in():
    return render_template("sign-in.html")

@app.route("/profile/<int:profile_id>")
def profile(profile_id):
    if profile_id == 1:
      return render_template("profile.html", user_profiles = profiles[0], profile_id=profile_id)
    elif profile_id == 2:
        return render_template("profile.html", user_profiles = profiles[1], profile_id=profile_id)
    return render_template("profile.html", user_profiles = profiles[2], profile_id=profile_id)



if __name__ == "__main__":
    app.run(debug=True)


