from models.base_model import BaseModel
from models.chef import Chef
from models.chef_menu import ChefMenu
import peewee as pw

class MenuImage(BaseModel):
    chef = pw.ForeignKeyField(Chef, backref="menu_images", on_delete="CASCADE")
    chef_menu = pw.ForeignKeyField(ChefMenu, backref="menu_images", on_delete="CASCADE")
    image_path = pw.TextField(null=True)

    
