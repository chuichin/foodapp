from models.base_model import BaseModel
from models.user import User
from models.review import Review
import peewee as pw

class ReviewImage(BaseModel):
    review = pw.ForeignKeyField(Review, backref="review_images", on_delete="CASCADE")
    user = pw.ForeignKeyField(User, backref="review_images", on_delete="CASCADE")
    image_url = pw.TextField(null=True)


