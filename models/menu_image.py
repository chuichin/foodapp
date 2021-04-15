from models.base_model import BaseModel
from models.chef import Chef
import peewee as pw

class MenuImage(BaseModel):
    chef = pw.ForeignKeyField(Chef, backref="menu_images", on_delete="CASCADE")
    image_url = pw.TextField(null=True)
    