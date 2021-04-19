from app import app # , csrf 
from flask_cors import CORS 

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
from foodapp_api.blueprints.chefs.views import chefs_api_blueprint
from foodapp_api.blueprints.users.views import users_api_blueprint
from foodapp_api.blueprints.bookings.views import bookings_api_blueprint
from foodapp_api.blueprints.reviews.views import reviews_api_blueprint
from foodapp_api.blueprints.likes.views import likes_api_blueprint
from foodapp_api.blueprints.review_images.views import review_images_api_blueprint
from foodapp_api.blueprints.food_categories.views import food_categories_api_blueprint
from foodapp_api.blueprints.menu_images.views import menu_images_api_blueprint
from foodapp_api.blueprints.chef_menu.views import menu_images_api_blueprint
from foodapp_api.blueprints.braintree.views import braintree_api_blueprint


app.register_blueprint(chefs_api_blueprint, url_prefix='/api/v1/chefs')
app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')
app.register_blueprint(bookings_api_blueprint, url_prefix='/api/v1/bookings')
app.register_blueprint(reviews_api_blueprint, url_prefix='/api/v1/reviews')
app.register_blueprint(review_images_api_blueprint, url_prefix='/api/v1/review_images')
app.register_blueprint(food_categories_api_blueprint, url_prefix='/api/v1/food_categories')
app.register_blueprint(menu_images_api_blueprint, url_prefix='/api/v1/menu_images')
app.register_blueprint(menu_images_api_blueprint, url_prefix='/api/v1/chef_menu')
app.register_blueprint(braintree_api_blueprint, url_prefix='/api/v1/payment')
