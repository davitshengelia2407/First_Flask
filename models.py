from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum
from enums import UserRole

from ext import db, login_manager


class BaseModel:

    def create(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def save():
        db.session.commit()

class Brand(db.Model, BaseModel):
    __tablename__ = "brands"

    id = db.Column(db.Integer(), primary_key = True)

    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)
    image = db.Column(db.String(), default="default_photo.jpg")

class User(db.Model, BaseModel, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key = True)
    image = db.Column(db.String)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    mobile_number = db.Column(db.String)
    role = db.Column(Enum(UserRole), nullable=False, default=UserRole.BASIC)

    def __init__(self, image, username, password, mobile_number, role='BASIC'):
        self.image = image
        self.username = username
        self.password = generate_password_hash(password)
        self.mobile_number = mobile_number
        self.role = role

    def check_hash(self, password):
        return check_password_hash(self.password, password)
    @property
    def is_admin(self):
        return self.role == UserRole.ADMIN

@login_manager.user_loader
def load_user(user_id):
    return User.query.get_or_404(user_id)
