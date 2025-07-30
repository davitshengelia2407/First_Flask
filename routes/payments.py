# routes/payment_routes.py

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from ext import db
from forms import CardAuthorizationForm
from models import Card

payment_bp = Blueprint('payment', __name__)

@payment_bp.route('/payment-methods')
@login_required
def payment_methods():
    cards = Card.query.filter_by(user_id=current_user.id).all()
    form = CardAuthorizationForm()
    return render_template('payment_methods.html', cards=cards, form=form)

@payment_bp.route('/add-card', methods=['POST'])
@login_required
def add_card():
    form = CardAuthorizationForm()
    if form.validate_on_submit():
        card_number = form.card_number.data.replace(" ", "").strip()
        expiry = form.expiry.data.strip()
        last_four = card_number[-4:]

        # Card brand detection
        if card_number.startswith('4'):
            brand = 'Visa'
        elif card_number[:2] in ['51', '52', '53', '54', '55']:
            brand = 'MasterCard'
        elif card_number.startswith('34') or card_number.startswith('37'):
            brand = 'American Express'
        elif card_number.startswith('6011') or card_number.startswith('65') or \
                (card_number[:3] >= '644' and card_number[:3] <= '649'):
            brand = 'Discover'
        else:
            brand = 'Unknown'

        # Prevent duplicates
        exists = Card.query.filter_by(
            user_id=current_user.id,
            card_number_last4=last_four,
            expiry=expiry
        ).first()
        if exists:
            flash('Card already exists.', 'warning')
            return redirect(url_for('payment.payment_methods'))

        new_card = Card(
            user_id=current_user.id,
            card_number_last4=last_four,
            card_brand=brand,
            expiry=expiry
        )
        db.session.add(new_card)
        db.session.commit()
        flash('Card added successfully.', 'success')
    else:
        flash('Invalid card data.', 'danger')

    return redirect(url_for('payment.payment_methods'))

