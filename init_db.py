from sqlalchemy import text
from enums import UserRole
from ext import app, db
from models import Brand, BaseModel, User

with app.app_context():
    # ✅ Verify connected DB name
    db_name = db.session.execute(text("SELECT current_database();")).scalar()
    print("🔌 Connected to DB:", db_name)

    # Reset tables
    db.drop_all()
    db.create_all()

    # Insert default admin
    admin = User(
        password='adminpass',
        username='admin',
        role=UserRole.ADMIN,
        image='5',
        mobile_number='5'
    )
    db.session.add(admin)
    db.session.commit()
