from flask import render_template, url_for, redirect, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from enums import UserRole
from forms import RegisterForm, AuctionForm, BrandForm, LoginForm, ProductForm
from os import path
import os
import glob
from app import app
from models import Brand, User, Product
from werkzeug.datastructures import FileStorage
from werkzeug.security import generate_password_hash, check_password_hash

footer_icons = [
    {"name": "Twitter", "filename": "twitter.png"},
    {"name": "Telegram", "filename": "telegram.png"},
    {"name": "Instagram", "filename": "instagram.png"},
    {"name": "GitHub", "filename": "github.png"}
]

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
@login_required
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
        existing_user = User.query.filter_by(username=form.username.data).first()
        if existing_user:
            flash("Username already taken, try another one.")
            return render_template("register.html", form=form)

        image = form.image.data
        filename = secure_filename(image.filename)
        directory = path.join(app.root_path, 'static', 'Images', 'Profile_photos', filename)
        image.save(directory)

        new_user = User(
            username=form.username.data,
            password=form.password.data,
            mobile_number=form.mobile_number.data,
            image=filename,
            role=UserRole.BASIC
        )
        User.create(new_user)

        return redirect(url_for("sign_in"))
    return render_template("register.html", form=form)

@app.route("/me")
@login_required
def me():
    user = current_user  # full user object
    return render_template("me.html", user=user)

@app.route("/add-brands", methods=["GET", "POST"])
@login_required
def add_brands():
    if current_user.role != UserRole.ADMIN:
        abort(403)
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
        print(form.errors)
        return redirect(url_for('auctions'))

    return render_template("add-auctions.html", form=form)


@app.route("/auctions")
@login_required
def auctions():
    return render_template("auctions.html")

@app.route("/brands/<int:id>")
def brand(id):
    return render_template(
        "brand.html",
        brand=Brand.query.get_or_404(id),  # passes one brand
    )

@app.route("/brands")
def all_brands():
    return render_template(
        "brands.html",
        brands= Brand.query.all(),
    )



@app.route("/brands/<int:id>/products")
def brand_products(id):
    brand_obj = Brand.query.get_or_404(id)
    products = brand_obj.products
    return render_template(
        "products.html",
        brand=brand_obj,
        products=products,
        role=current_user.role if current_user.is_authenticated else None
    )




@app.route("/profile/<int:profile_id>")
@login_required
def profile(profile_id):
    user = User.query.get_or_404(profile_id)
    return render_template("profile.html", user=user)

@app.route("/delete-brand/<int:id>")
@login_required
def delete_brand(id):
    if current_user.role != UserRole.ADMIN:
        abort(403)
    brand_obj = Brand.query.get(id)
    if not brand_obj:
        return "Brand not found", 404
    Brand.delete(brand_obj)
    return redirect(url_for('all_brands'))




@app.route("/edit-brand/<int:id>", methods=["GET", "POST"])
@login_required
def edit_brand(id):
    if current_user.role != UserRole.ADMIN:
        abort(403)
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

@app.route("/add-product", methods=["GET", "POST"])
@login_required
def add_product():
    if current_user.role != UserRole.ADMIN:
        abort(403)
    form = ProductForm()

    form.product_brand.choices = [(b.id, b.name) for b in Brand.query.all()]

    if form.validate_on_submit():
        image = form.image.data
        filename = secure_filename(image.filename)
        image_path = path.join(app.root_path, "static", "Images", "Brand_Products", filename)
        image.save(image_path)

        new_product = Product(
            name=form.product_name.data,
            description=form.product_desc.data,
            image=filename,
            price=form.product_price.data,
            discount_price=form.discount_price.data or None,
            stock=form.product_stock.data,
            type=form.product_type.data,
            brand_id=form.product_brand.data
        )

        Product.create(new_product)
        return redirect(url_for("home"))

    return render_template("add-product.html", form=form)
