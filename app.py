from flask import Flask, render_template
from sqlalchemy.sql.functions import count

from forms import  RegisterForm
from os import path

app = Flask(__name__)
app.config["SECRET_KEY"] = "daculisaiti"

import os
import glob

import os
import glob

upload_folder = os.path.join(app.root_path, 'static', 'Images', 'Profile_Photos')

# Delete all files in the upload folder
for file_path in glob.glob(os.path.join(upload_folder, '*')):
    try:
        os.remove(file_path)
        print(f"Deleted {file_path}")
    except Exception as e:
        print(f"Error deleting {file_path}: {e}")


brands = [
    {
        "id": 1,
        "name": "La-Roche Posay",
        "image": "larocheposay.png",
        "description": "A dermatologist-recommended skincare brand offering effective, gentle formulas with antioxidant-rich thermal spring water, ideal for sensitive, acne-prone, or reactive skin."
    },
    {
        "id": 2,
        "name": "Cetaphil",
        "image": "cetaphil_logo.jpg",
        "description": "Cetaphil is a gentle, dermatologist-recommended skincare brand formulated for sensitive skin, offering effective cleansers and moisturizers that hydrate, soothe, and protect the skin barrier."
    },
    {
        "id": 3,
        "name": "The Ordinary",
        "image": "theordinary_logo.svg",
        "description": "The Ordinary offers clinical skincare with integrity, featuring potent active ingredients in minimalist formulas at affordable prices—ideal for targeted treatments like retinol, niacinamide, and acids."
    },
    {
        "id": 4,
        "name": "Cerave",
        "image": "cerave_logo.png",
        "description": "CeraVe is a dermatologist-developed skincare brand known for gentle, effective ceramide-rich formulas that restore and protect the skin barrier—perfect for dry, sensitive, or acne-prone skin."
    },
    {
        "id": 5,
        "name": "Dermedic",
        "image": "dermedic.png",
        "description": "Dermedic creates dermatologically-tested skincare for sensitive, dry, or problematic skin, using thermal water and hypoallergenic ingredients for hydration, repair, and long-term comfort."
    },
    {
        "id": 6,
        "name": "Avene",
        "image": "avene_logo.png",
        "description": "Avène specializes in soothing skincare powered by thermal spring water, clinically proven to calm sensitive, irritated, or reactive skin—recommended by dermatologists worldwide for daily gentle care."
    },
    {
        "id": 7,
        "name": "Vichy",
        "image": "vichy.jpg",
        "description": "Vichy is a French skincare brand using volcanic thermal water and active ingredients to strengthen, hydrate, and visibly improve skin health—ideal for sensitive, aging, or stressed skin."
    },
    {
        "id": 8,
        "name": "Ahava",
        "image": "ahava.webp",
        "description": "AHAVA formulates mineral-rich skincare from Dead Sea ingredients, delivering natural hydration, rejuvenation, and nourishment—ideal for dry, mature, or stressed skin seeking clean, effective solutions."
    },
    {
        "id": 9,
        "name": "Cliven",
        "image": "cliven.png",
        "description": "Cliven blends tradition with modern science, offering premium body and skincare products enriched with natural extracts—focusing on gentle care, nourishment, and daily skin wellness."
    },
    {
        "id": 10,
        "name": "Nuxe",
        "image": "nuxe.png",
        "description": "Nuxe combines natural botanicals with luxurious textures to create effective, sensorial skincare—famous for its Huile Prodigieuse and formulas that nourish, hydrate, and enhance skin radiance."
    },
    {
        "id": 11,
        "name": "Topicrem",
        "image": "topicrem.png",
        "description": "Topicrem offers dermatologist-tested skincare for sensitive, dry, or atopic skin, providing effective gentle hydration, barrier repair, and soothing relief for all ages, including babies and adults."
    },
    {
        "id": 12,
        "name": "Bioderma",
        "image": "bioderma.png",
        "description": "Bioderma is a science-driven skincare brand known for micellar water and skin biology-based formulas that support healthy, balanced skin—ideal for sensitive, oily, or reactive skin types."
    }
]

footer_icons = [
    {"name": "Twitter", "filename": "twitter.png"},
    {"name": "Telegram", "filename": "telegram.png"},
    {"name": "Instagram", "filename": "instagram.png"},
    {"name": "GitHub", "filename": "github.png"}
]

products = [
    {
        "id": 1,
        "type": "moisturizer",
        "name": "Lipikar ap +m",
        "description": "Dermatologist-tested, this body cream is safe for the whole family’s sensitive skin. It is suitable for patients undergoing chemotherapy and radiation*, helping moisturize and comfort sensitive skin.",
        "image": ""
    },
    {
        "id": 2,
        "type": "sunscreen",
        "name": "Anthelios Spf50+",
        "description": "Anthelios UV Pro-Sport Sunscreen SPF 50 provides high-endurance, water-resistant protection against 98% of UVB rays with Cell-Ox Shield® Technology. Broad-spectrum sunscreen has a breathable texture.",
        "image": ""
    }

]

profiles = [
    {
        "id": 1,  "name": "davit", "surname": "shengelia", "image": "skami.jpg"
    },
    {
        "id": 2,  "name": "ana", "surname": "iarajuli", "image": "magida.png"
    },
    {
        "id": 3,  "name": "ana", "surname": "grdzelishvili", "image": "plates.webp"
    }
]

users = []

role = "user"

@app.context_processor
def inject_footer_icons():
    return dict(footer_icons=footer_icons)

@app.route("/")
def home():
    return render_template("index.html", brands = brands)

@app.route("/brands/<int:brand_id>")
def brand(brand_id):
    return render_template(
        "brands.html",
        brand=brands[brand_id - 1],  # passes one brand
        role=role
    )

@app.route("/brands/<int:brand_id>/products")
def brand_products(brand_id):
    return render_template(
        "products.html",
        brand=brands[brand_id - 1],
        role=role,
        products=products  # pass the products list
    )


@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/register", methods = ["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = {
            "username": form.username.data,
            "password": form.password.data,
            "birthdate": form.birthdate.data,
            "mobile_number": form.mobile_number.data,
            "gender": form.gender.data,
            "country": form.country.data
        }
        image = form.image.data
        directory = path.join(app.root_path, 'static', 'Images', 'Profile_Photos', image.filename)
        image.save(directory)
        new_user["profile_image"] = image.filename
        users.append(new_user)
        print(users)
    print(form.errors)
    return render_template("register.html", form = form)

@app.route("/log-in")
@app.route("/sign-in")
def sign_in():
    return render_template("sign-in.html")

@app.route("/profile/<int:profile_id>")
def profile(profile_id):
    return render_template("profile.html", user_profiles = users[profile_id], profile_id=profile_id)



if __name__ == "__main__":
    app.run(debug=True)


