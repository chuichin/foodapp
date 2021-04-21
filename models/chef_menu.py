from models.base_model import BaseModel
from models.food_category import FoodCategory
import peewee as pw

class ChefMenu(BaseModel):
    food_category = pw.ForeignKeyField(FoodCategory, backref="menus", on_delete="CASCADE")
    appetiser = pw.TextField(null=False)
    main = pw.TextField(null=False)
    dessert = pw.TextField(null=False)