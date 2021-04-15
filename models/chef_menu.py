from models.base_model import BaseModel
from models.food_category import FoodCategory
import peewee as pw

class ChefMenu(BaseModel):
    food_category = pw.ForeignKeyField(FoodCategory, backref="menus", on_delete="CASCADE")
    menu = pw.TextField(null=False)