from models.base_model import BaseModel
from models.user import User
from models.chef import Chef
import peewee as pw

class Like(BaseModel):
    user = pw.ForeignKeyField(User, backref="likes",  on_delete="CASCADE")
    chef = pw.ForeignKeyField(Chef, backref="likes", on_delete="CASCADE")

