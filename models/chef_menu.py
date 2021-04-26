from models.base_model import BaseModel
from models.food_category import FoodCategory
from models.chef import Chef
import peewee as pw

class ChefMenu(BaseModel):
    chef = pw.ForeignKeyField(Chef, backref="menus",  on_delete="CASCADE")
    food_category = pw.TextField(null=True)
    appetiser = pw.TextField(null=True)
    main = pw.TextField(null=True)
    starter =pw.TextField(null=True)
    dessert = pw.TextField(null=True)
    description = pw.TextField(null=True)
    