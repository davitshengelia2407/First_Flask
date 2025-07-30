from flask import render_template, url_for, redirect, flash, abort, request, Blueprint, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from flask_migrate import check
from werkzeug.exceptions import InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from utils.aws.s3services import upload_file_to_s3
from utils.card_utils import detect_card_brand
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage


from enums import UserRole
from ext import db
from forms import RegisterForm, AuctionForm, BrandForm, LoginForm, ProductForm, CardAuthorizationForm, ChangePasswordForm
from os import path
import os
import glob
from app import app
from models import Brand, User, Product, Auction, Card
from werkzeug.datastructures import FileStorage

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
            next_page = request.args.get('next')
            flash("signed-in successfully")
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
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
        if User.query.filter_by(username=form.username.data).first():
            flash("Username already taken, try another one.", "danger")
            return render_template("register.html", form=form)

        image = form.image.data
        if not image:
            flash("Profile image is required.", "danger")
            return render_template("register.html", form=form)

        try:
            s3_url = upload_file_to_s3(image, folder="Profile_photos")
        except Exception as e:
            app.logger.error(f"S3 upload failed: {e}")
            raise InternalServerError("Could not upload image. Try again later.")

        new_user = User(
            username=form.username.data,
            password=form.password.data,
            mobile_number=form.mobile_number.data,
            image=s3_url,
            role=UserRole.BASIC
        )
        User.create(new_user)

        flash("Account created successfully. You can now sign in.", "success")
        return redirect(url_for("sign_in"))

    return render_template("register.html", form=form)

@app.route("/me", methods=["GET", "POST"])
@login_required
def me():
    form = ChangePasswordForm()

    if form.validate_on_submit():
        if not current_user.check_hash(form.old_password.data):
            flash("Ძველი პაროლი არასწორია", "danger")
        elif form.new_password.data != form.confirm_password.data:
            flash("Პაროლები არ ემთხვევა", "danger")
        else:
            current_user.password = form.new_password.data  # uses model's setter
            db.session.commit()
            flash("Პაროლი წარმატებით შეიცვალა", "success")
            return redirect(url_for("me"))

    return render_template("me.html", user=current_user, form=form)



@app.route("/add-brands", methods=["GET", "POST"])
@login_required
def add_brands():
    if current_user.role != UserRole.ADMIN:
        abort(403)

    form = BrandForm(require_image=True)
    if form.validate_on_submit():
        image = form.image.data
        if not image:
            flash("Brand image is required.", "danger")
            return render_template("add-brands.html", form=form)

        try:
            s3_url = upload_file_to_s3(image, folder="Brand_Logos")
        except Exception as e:
            app.logger.error(f"S3 upload failed: {e}")
            raise InternalServerError("Could not upload image. Try again later.")

        new_brand = Brand(
            name=form.name.data,
            description=form.description.data,
            image=s3_url  # ✅ store S3 URL
        )
        Brand.create(new_brand)
        return redirect(url_for('all_brands'))

    return render_template("add-brands.html", form=form)

@app.route("/add-auctions", methods=["GET", "POST"])
@login_required
def add_auction():
    form = AuctionForm()

    if form.validate_on_submit():
        image = form.image.data
        if not image:
            flash("Auction image is required.", "danger")
            return render_template("add-auctions.html", form=form)

        try:
            s3_url = upload_file_to_s3(image, folder="Auctions")
        except Exception as e:
            app.logger.error(f"S3 upload failed during auction creation: {e}")
            flash("Image upload failed. Please try again.", "danger")
            return render_template("add-auctions.html", form=form)

        auction = Auction(
            product_name=form.product_name.data,
            description=form.description.data,
            image=s3_url,
            price=form.price.data,
            type=form.type.data,
            user_id=current_user.id
        )

        Auction.create(auction)
        flash("Auction added successfully.", "success")
        return redirect(url_for('auctions'))

    return render_template("add-auctions.html", form=form)


@app.route("/auctions")
@login_required
def auctions():
    all_auctions = Auction.query.order_by(Auction.created_at.desc()).all()
    return render_template("auctions.html", auctions=all_auctions)


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

from werkzeug.datastructures import FileStorage

@app.route("/edit-brand/<int:id>", methods=["GET", "POST"])
@login_required
def edit_brand(id):
    if current_user.role != UserRole.ADMIN:
        abort(403)

    brand_obj = Brand.query.get_or_404(id)
    form = BrandForm(obj=brand_obj, require_image=False)
    form.submit_brand.label.text = "Update Brand"

    if form.validate_on_submit():
        brand_obj.name = form.name.data
        brand_obj.description = form.description.data

        if isinstance(form.image.data, FileStorage) and form.image.data.filename:
            try:
                s3_url = upload_file_to_s3(form.image.data, folder="Brand_Logos")
                brand_obj.image = s3_url
            except Exception as e:
                app.logger.error(f"S3 upload failed during brand edit: {e}")
                flash("Image upload failed. Please try again.", "danger")
                return render_template('edit-brand.html', form=form, brand=brand_obj)

        brand_obj.save()
        flash("Brand updated successfully.", "success")
        return redirect(url_for('brand', id=brand_obj.id))

    return render_template('edit-brand.html', form=form, brand=brand_obj)


@app.route("/add-product", methods=["GET", "POST"])
@login_required
def add_product():
    if current_user.role != UserRole.ADMIN:
        abort(403)

    form = ProductForm(require_image=True)
    form.brand.choices = [(b.id, b.name) for b in Brand.query.all()]

    if form.validate_on_submit():
        image = form.image.data
        if not image:
            flash("Product image is required.", "danger")
            return render_template("add-product.html", form=form)

        try:
            s3_url = upload_file_to_s3(image, folder="Brand_Products")
        except Exception as e:
                      app.logger.error(f"S3 upload failed: {e}")
                      raise InternalServerError("Could not upload image. Try again later.")

        new_product = Product(
            name=form.name.data,
            description=form.description.data,
            image=s3_url,
            price=form.price.data,
            discount_price=form.discount_price.data or None,
            stock=form.stock.data,
            type=form.type.data,
            brand_id=form.brand.data
        )

        Product.create(new_product)
        return redirect(url_for("home"))

    return render_template("add-product.html", form=form)

# @app.route("/add-brands", methods=["GET", "POST"])
# @login_required
# def add_brands():
#     if current_user.role != UserRole.ADMIN:
#         abort(403)
#
#     form = BrandForm(require_image=True)
#     if form.validate_on_submit():
#         image = form.image.data
#         if not image:
#             flash("Brand image is required.", "danger")
#             return render_template("add-brands.html", form=form)
#
#         try:
#             s3_url = upload_file_to_s3(image, folder="Brand_Logos")
#         except Exception as e:
#             app.logger.error(f"S3 upload failed: {e}")
#             raise InternalServerError("Could not upload image. Try again later.")
#
#         new_brand = Brand(
#             name=form.name.data,
#             description=form.description.data,
#             image=s3_url  # ✅ store S3 URL
#         )
#         Brand.create(new_brand)
#         return redirect(url_for('all_brands'))
#
#     return render_template("add-brands.html", form=form)

@app.route("/brands/<int:brand_id>/products/<int:product_id>")
def single_product(brand_id, product_id):
    brand_obj = Brand.query.get_or_404(brand_id)
    product_obj = Product.query.filter_by(id=product_id, brand_id=brand_id).first_or_404()

    return render_template("single-product.html", one_product=product_obj, brand=brand_obj)


@app.route("/brands/<int:brand_id>/products/edit/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(brand_id, product_id):
    if current_user.role != UserRole.ADMIN:
        abort(403)

    brand_obj = Brand.query.get_or_404(brand_id)
    product_obj = Product.query.filter_by(id=product_id, brand_id=brand_id).first_or_404()

    form = ProductForm(obj=product_obj)
    form.submit_product.label.text = "Update Product"
    form.brand.choices = [(brand_obj.id, brand_obj.name)]
    form.brand.data = brand_obj.id
    form.brand.render_kw = {"readonly": True, "disabled": True}

    if form.validate_on_submit():
        product_obj.name = form.name.data
        product_obj.description = form.description.data
        product_obj.price = form.price.data
        product_obj.discount_price = form.discount_price.data
        product_obj.stock = form.stock.data
        product_obj.type = form.type.data

        if isinstance(form.image.data, FileStorage) and form.image.data.filename:
            try:
                s3_url = upload_file_to_s3(form.image.data, folder="Brand_Products")
                product_obj.image = s3_url
            except Exception as e:
                app.logger.error(f"S3 upload failed during product edit: {e}")
                flash("Image upload failed. Please try again.", "danger")
                return render_template('edit-product.html', form=form, product=product_obj, brand=brand_obj)

        product_obj.save()
        flash("Product updated successfully.", "success")
        return redirect(url_for('single_product', brand_id=brand_id, product_id=product_id))

    return render_template('edit-product.html', form=form, product=product_obj, brand=brand_obj)

@app.route("/product/<int:product_id>/delete", methods=["POST", "GET"])
@login_required
def delete_product(product_id):
    if not current_user.is_admin:
        abort(403)

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted.", "success")
    return redirect(url_for("home"))



@app.route("/api/search_suggestions")
def search_suggestions():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([])

    products = Product.query.filter(
        Product.name.ilike(f"%{query}%")
    ).limit(5).all()

    return jsonify([
        {
            "name": p.name,
            "image": p.image,  # AWS URL
            "brand_id": p.brand_id,
            "product_id": p.id,
            "price": f"${p.price:.2f}"
        } for p in products
    ])

@app.route("/search")
def search_results():
    query = request.args.get("q", "").strip()
    if not query:
        flash("No search term provided.", "warning")
        return redirect(url_for("index"))

    products = Product.query.filter(Product.name.ilike(f"%{query}%")).all()
    return render_template("search_results.html", query=query, products=products)






