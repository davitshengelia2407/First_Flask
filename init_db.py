from enums import UserRole
from ext import app, db

from models import Brand, BaseModel, User

with app.app_context():
    db.drop_all()
    db.create_all()


    admin = User(password='adminpass', username='admin', role=UserRole.ADMIN, image='5', mobile_number='5')
    db.session.add(admin)
    db.session.commit()
