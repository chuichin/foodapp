from models.base_model import BaseModel
from models.food_category import FoodCategory
from models.chef import Chef
import peewee as pw

class ChefMenu(BaseModel):
    chef = pw.ForeignKeyField(Chef, backref="menus",  on_delete="CASCADE")
    # food_category = pw.ForeignKeyField(FoodCategory, backref="menus", on_delete="CASCADE")
    appetiser = pw.TextField(null=False)
    main = pw.TextField(null=False)
    dessert = pw.TextField(null=False)
