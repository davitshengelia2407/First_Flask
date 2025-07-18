from ext import db
from app import app
from models import User, Brand, Product, Auction, Basket, BasketItem
from enums import UserRole

from werkzeug.security import generate_password_hash

with app.app_context():
    # Clear existing data (optional in dev only)
    BasketItem.query.delete()
    Basket.query.delete()
    Auction.query.delete()
    Product.query.delete()
    Brand.query.delete()
    User.query.delete()
    db.session.commit()

    # Users
    admin = User(username="admin", mobile_number="555123", role=UserRole.ADMIN)
    admin.password = "admin123"
    user = User(username="user", mobile_number="555456", role=UserRole.BASIC)
    user.password = "user123"
    db.session.add_all([admin, user])
    db.session.commit()

    # Brand
    brand = Brand(name="La Roche-Posay", description="Test brand", image="default_photo.jpg")
    db.session.add(brand)
    db.session.commit()

    # Product
    product = Product(
        name="Hydrating Cream",
        description="Moisturizing cream for dry skin",
        image="product1.jpg",
        price=100,
        discount_price=90,
        stock=20,
        type="დამატენიანებელი",
        brand_id=brand.id
    )
    db.session.add(product)
    db.session.commit()

    # Auction
    auction = Auction(
        product_name="Rare SPF 50",
        description="Auction product",
        image="auction1.jpg",
        price=120,
        type="მზისგან დამცავი",
        user_id=admin.id
    )
    db.session.add(auction)
    db.session.commit()

    # Basket
    basket = Basket(user_id=user.id)
    db.session.add(basket)
    db.session.commit()

    # BasketItem
    item = BasketItem(basket_id=basket.id, product_id=product.id, quantity=2)
    db.session.add(item)
    db.session.commit()

    print("✅ Dummy data seeded.")
