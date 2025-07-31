from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_required, current_user
from werkzeug.exceptions import abort

from ext import db
from models import Basket, BasketItem, Product

basket_bp = Blueprint("basket", __name__)


@basket_bp.route("/basket")
@login_required
def view_basket():
    basket = Basket.query.filter_by(user_id=current_user.id).first()
    items = []

    if basket:
        items = (
            BasketItem.query
            .filter_by(basket_id=basket.id)
            .order_by(BasketItem.created_at.desc())
            .all()
        )

    total = sum(item.product.price * item.quantity for item in items)
    return render_template("basket.html", basket=basket, items=items, total=total)



@basket_bp.route("/basket/add/<int:product_id>", methods=["POST"])
def add_to_basket(product_id):
    if not current_user.is_authenticated:
        # Save product info + next URL in session before redirecting to login
        session["pending_product_id"] = product_id
        session["next_after_login"] = request.form.get("next") or url_for("main.home")
        return redirect(url_for("sign_in"))

    product = Product.query.get_or_404(product_id)
    brand_id = request.form.get("brand_id")

    basket = Basket.query.filter_by(user_id=current_user.id).first()
    if not basket:
        basket = Basket(user_id=current_user.id)
        db.session.add(basket)
        db.session.commit()

    item = next((i for i in basket.items if i.product_id == product.id), None)
    if item:
        item.quantity += 1
    else:
        item = BasketItem(basket_id=basket.id, product_id=product.id, quantity=1)
        db.session.add(item)

    db.session.commit()
    flash("Product added to basket!", "success")
    next_url = request.form.get("next") or url_for("product.single_product", brand_id=brand_id, product_id=product_id)
    return redirect(next_url)




@basket_bp.route("/basket/remove/<int:item_id>", methods=["POST"])
@login_required
def remove_from_basket(item_id):
    item = BasketItem.query.get_or_404(item_id)
    if item.basket.user_id != current_user.id:
        abort(403)

    db.session.delete(item)
    db.session.commit()
    flash("Item removed from basket.", "info")
    return redirect(url_for("basket.view_basket"))


@basket_bp.route("/basket/decrease/<int:item_id>", methods=["POST"])
@login_required
def decrease_item_quantity(item_id):
    item = BasketItem.query.get_or_404(item_id)
    if item.basket.user_id != current_user.id:
        abort(403)

    if item.quantity > 1:
        item.quantity -= 1
    else:
        db.session.delete(item)

    db.session.commit()
    return redirect(url_for("basket.view_basket"))


@basket_bp.route("/basket/increase/<int:item_id>", methods=["POST"])
@login_required
def increase_item_quantity(item_id):
    item = BasketItem.query.get_or_404(item_id)
    if item.basket.user_id != current_user.id:
        abort(403)

    item.quantity += 1
    db.session.commit()
    return redirect(url_for("basket.view_basket"))
