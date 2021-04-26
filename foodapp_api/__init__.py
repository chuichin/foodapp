from app import app # , csrf 
from flask_cors import CORS 

cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

## API Routes ##
from foodapp_api.blueprints.chefs.views import chefs_api_blueprint
from foodapp_api.blueprints.user.views import users_api_blueprint
from foodapp_api.blueprints.bookings.views import bookings_api_blueprint
from foodapp_api.blueprints.review.views import reviews_api_blueprint
from foodapp_api.blueprints.likes.views import likes_api_blueprint
# from foodapp_api.blueprints.review_images.views import review_images_api_blueprint
from foodapp_api.blueprints.food_categories.views import food_categories_api_blueprint
from foodapp_api.blueprints.menu_images.views import menu_images_api_blueprint
from foodapp_api.blueprints.chef_menu.views import chef_menu_api_blueprint
from foodapp_api.blueprints.braintree.views import braintree_api_blueprint
from foodapp_api.blueprints.search.views import search_api_blueprint
from foodapp_api.blueprints.notifications.views import notifications_api_blueprint



app.register_blueprint(chefs_api_blueprint, url_prefix='/api/v1/chefs')
app.register_blueprint(users_api_blueprint, url_prefix='/api/v1/users')
app.register_blueprint(bookings_api_blueprint, url_prefix='/api/v1/bookings')
app.register_blueprint(reviews_api_blueprint, url_prefix='/api/v1/reviews')
app.register_blueprint(likes_api_blueprint, url_prefix='/api/v1/likes')
# app.register_blueprint(review_images_api_blueprint, url_prefix='/api/v1/review_images')
app.register_blueprint(food_categories_api_blueprint, url_prefix='/api/v1/food_categories')
app.register_blueprint(menu_images_api_blueprint, url_prefix='/api/v1/menu_images')
app.register_blueprint(chef_menu_api_blueprint, url_prefix='/api/v1/menus')
app.register_blueprint(braintree_api_blueprint, url_prefix='/api/v1/payments')
app.register_blueprint(search_api_blueprint, url_prefix='/api/v1/searches')
app.register_blueprint(notifications_api_blueprint, url_prefix='/api/v1/notifications')


