from ext import  app
from ext import app
from models import Brand, User, BaseModel, UserMixin, Product
import models



if __name__ == "__main__":
    from routes import single_product, inject_footer_icons, home, register, add_auction, auctions, brand, brand_products, sign_in, add_product, add_brands, me
    from routes.basket import view_basket, remove_from_basket, add_to_basket
    app.run(debug=True)


