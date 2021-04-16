from models.base_model import BaseModel
from models.user import User
from models.chef import Chef
import peewee as pw

class Review(BaseModel):
    user=pw.ForeignKeyField(User, backref='reviews', on_delete="CASCADE")
    chef=pw.ForeignKeyField(Chef, backref='reviews', on_delete="CASCADE")
    comment=pw.TextField(default=None)
    rating=pw.FloatField(default=None)

