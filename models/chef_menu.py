from models.base_model import BaseModel
from models.food_category import FoodCategory
from models.chef import Chef
import peewee as pw

class ChefMenu(BaseModel):
    chef = pw.ForeignKeyField(Chef, backref="menus",  on_delete="CASCADE")
    food_category = pw.TextField(null=False)
    menu = pw.TextField(null=False)