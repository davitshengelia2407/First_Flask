from ext import  app
from ext import app
from models import Brand, User, BaseModel, UserMixin
import models


if __name__ == "__main__":
    from routes import delete_files_in_folder, inject_footer_icons, home, register, add_auction, auctions, brand, brand_products, sign_in, products
    app.run(debug=True)


