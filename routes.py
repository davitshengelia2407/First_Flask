from flask import render_template, url_for, redirect, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from forms import RegisterForm, AuctionForm, BrandForm, LoginForm
from os import path
import os
import glob
from app import app
from models import Brand, User
from werkzeug.datastructures import FileStorage
from werkzeug.security import generate_password_hash, check_password_hash

profile_folder = os.path.join(app.root_path, 'static', 'Images', 'Profile_Photos')
auction_folder = os.path.join(app.root_path, 'static', 'Images', 'Auctions')

def delete_files_in_folder(folder_path):
    for file_path in glob.glob(os.path.join(folder_path, '*')):
        try:
            os.remove(file_path)
            print(f"Deleted {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

delete_files_in_folder(profile_folder)
delete_files_in_folder(auction_folder)


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
auction_products = []

role = "admin"

@app.context_processor
def inject_footer_icons():
    return dict(footer_icons=footer_icons)

@app.route("/")
def home():
    return render_template(
        "index.html",
        brands = Brand.query.all()
    )

@app.route("/sign-in", methods = ['GET', 'POST'])
def sign_in():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and user.check_hash(form.password.data):
            login_user(user)
            flash('signed-in successfuly')
            return redirect(url_for('home'))
        else:
            flash("couldn't sign in")
    return render_template("sign-in.html", form = form)

@app.route('/sign-out')
def sign_out():
    logout_user()
    flash('signed-out succesfuly')
    return redirect(url_for('home'))

@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegisterForm()
    if form.validate_on_submit():
        image = form.image.data
        filename = secure_filename(image.filename)
        directory = path.join(app.root_path, 'static', 'Images', 'Profile_photos', filename)
        image.save(directory)
        new_user = User(
            username=form.username.data,
            password=form.password.data,
            mobile_number=form.mobile_number.data,
            image=filename        )
        User.create(new_user)

        return redirect(url_for("home"))
    return render_template("register.html", form=form)


@app.route("/add-brands", methods=["GET", "POST"])
@login_required
def add_brands():
    form = BrandForm()
    if form.validate_on_submit():
        new_brand = Brand(name=form.name.data, description=form.description.data)
        image = form.image.data
        filename = secure_filename(image.filename)
        directory = path.join(app.root_path, "static", "Images", "Brand_Logos", filename )
        image.save(directory)
        new_brand.image = filename
        Brand.create(new_brand)
        return redirect(url_for('all_brands'))
    return render_template("add-brands.html", form=form)


@app.route("/add-auctions", methods=["GET", "POST"])
@login_required
def add_auction():
    form = AuctionForm()
    if form.validate_on_submit():
        new_product = {
            "product_name": form.product_name.data,
            "description": form.description.data,
            "type": form.type.data
        }
        image = form.image.data
        filename = secure_filename(image.filename)
        directory = path.join(app.root_path, 'static', 'Images', 'Auctions', filename)
        image.save(directory)
        new_product["image"] = filename
        auction_products.append(new_product)
        print(auction_products)
        print(form.errors)
        return redirect(url_for('auctions'))

    return render_template("add-auctions.html", form=form)


@app.route("/auctions")
@login_required
def auctions():
    return render_template("auctions.html", auction_products = auction_products)

@app.route("/brands/<int:id>")
def brand(id):
    return render_template(
        "brand.html",
        brand=Brand.query.get_or_404(id),  # passes one brand
        role=role
    )

@app.route("/brands")
def all_brands():
    return render_template(
        "brands.html",
        brands= Brand.query.all(),
        role=role
    )



@app.route("/brands/<int:id>/products")
def brand_products(id):
    return render_template(
        "products.html",
        brand= Brand.query.get_or_404(id),
        role=role,
        products=products
    )

@app.route("/profile/<int:profile_id>")
@login_required
def profile(profile_id):
    user = User.query.get_or_404(profile_id)
    return render_template("profile.html", user=user)

@app.route("/delete-brand/<int:id>")
@login_required
def delete_brand(id):
    brand_id = Brand.query.get(id)
    if not brand_id:
        return "Brand not found", 404
    brand_id.delete()
    return redirect(url_for('all_brands'))




@app.route("/edit-brand/<int:id>", methods=["GET", "POST"])
@login_required
def edit_brand(id):
    brand_obj = Brand.query.get_or_404(id)
    form = BrandForm(obj=brand_obj)
    form.submit_brand.label.text = "შეცვალე ბრენდი"

    if form.validate_on_submit():
        brand_obj.name = form.name.data
        brand_obj.description = form.description.data

        if isinstance(form.image.data, FileStorage) and form.image.data.filename:
            filename = secure_filename(form.image.data.filename)
            filepath = os.path.join(app.root_path, "static", "Images", "Brand_Logos", filename)
            form.image.data.save(filepath)
            brand_obj.image = filename

        Brand.save()
        return redirect(url_for('brand', id=brand_obj.id))

    return render_template('edit-brand.html', form=form, brand=brand_obj)

