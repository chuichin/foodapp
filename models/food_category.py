from models.base_model import BaseModel
from models.chef import Chef
import peewee as pw

class FoodCategory(BaseModel):
    chef = pw.ForeignKeyField(Chef, backref="categories",  on_delete="CASCADE")
    category = pw.TextField(null=False)