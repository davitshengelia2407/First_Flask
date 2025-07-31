from datetime import datetime, timezone, UTC
from email.policy import default

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum
from enums import UserRole

from ext import db, login_manager


class BaseModel:
    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def save():
        db.session.commit()

    def to_dict(self):
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
        }


class User(db.Model, BaseModel, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    _password = db.Column("password", db.String(255), nullable=False)
    mobile_number = db.Column(db.String(20))
    image = db.Column(db.String(255), default="default_user.jpg")
    role = db.Column(Enum(UserRole), nullable=False, default=UserRole.BASIC)

    @property
    def password(self):
        raise AttributeError("Password is write-only.")

    @password.setter
    def password(self, raw_password):
        self._password = generate_password_hash(raw_password)

    def check_hash(self, raw_password):
        return check_password_hash(self._password, raw_password)

    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

    def to_dict(self):
        data = super().to_dict()
        data.pop("password", None)
        return data


@login_manager.user_loader
def load_user(user_id):
    return User.query.get_or_404(user_id)


class Brand(db.Model, BaseModel):
    __tablename__ = "brands"

    id = db.Column(db.Integer(), primary_key = True)

    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    image = db.Column(db.String(), default="default_photo.jpg")
    products = db.relationship('Product', backref='brand', lazy=True)

class Product(db.Model, BaseModel):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    discount_price = db.Column(db.Float, nullable=True)
    stock = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    hidden = db.Column(db.Boolean, default=False)
    purchased_times = db.Column(db.Integer, default=0)
    brand_id = db.Column(db.Integer, db.ForeignKey('brands.id'), nullable=False)


class Basket(db.Model, BaseModel):
    __tablename__ = "baskets"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

    user = db.relationship('User', backref=db.backref('basket', uselist=False))
    items = db.relationship(
        'BasketItem',
        backref='basket',
        lazy=True,
        cascade="all, delete-orphan"
    )


class BasketItem(db.Model, BaseModel):
    __tablename__ = "basket_items"

    id = db.Column(db.Integer, primary_key=True)
    basket_id = db.Column(db.Integer, db.ForeignKey('baskets.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime(timezone=True), default=lambda: datetime.now(UTC))

    product = db.relationship('Product')


class Auction(db.Model, BaseModel):
    __tablename__ = "auctions"

    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(50), nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship("User", backref="auctions")


class Card(db.Model, BaseModel):
    __tablename__ = 'cards'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    card_number_last4 = db.Column(db.String(4), nullable=False)
    card_brand = db.Column(db.String(20), nullable=False)
    expiry = db.Column(db.String(5), nullable=False)
    token = db.Column(db.String(255), nullable=True)

    user = db.relationship('User', backref='cards')

    __table_args__ = (
        db.UniqueConstraint('user_id', 'card_number_last4', 'expiry', name='unique_user_card'),
    )



