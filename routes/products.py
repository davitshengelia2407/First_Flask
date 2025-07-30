from flask import Blueprint, flash, render_template, url_for
from flask_login import login_required, current_user
from werkzeug.datastructures import FileStorage
from werkzeug.exceptions import abort, InternalServerError
from werkzeug.utils import redirect

from enums import UserRole
from ext import app, db
from forms import ProductForm
from models import Brand, Product
from utils.aws.s3services import upload_file_to_s3

product_bp = Blueprint("product", __name__)

@product_bp.route("/brands/<int:brand_id>/products/edit/<int:product_id>", methods=["GET", "POST"])
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

        return redirect(url_for('product.single_product', brand_id=brand_id, product_id=product_id))

    return render_template('edit-product.html', form=form, product=product_obj, brand=brand_obj)

@product_bp.route("/product/<int:product_id>/delete", methods=["POST", "GET"])
@login_required
def delete_product(product_id):
    if not current_user.is_admin:
        abort(403)

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted.", "success")
    return redirect(url_for("home"))

@product_bp.route("/brands/<int:brand_id>/products/<int:product_id>")
def single_product(brand_id, product_id):
    brand_obj = Brand.query.get_or_404(brand_id)
    product_obj = Product.query.filter_by(id=product_id, brand_id=brand_id).first_or_404()

    return render_template("single-product.html", one_product=product_obj, brand=brand_obj)



@product_bp.route("/add-product", methods=["GET", "POST"])
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
