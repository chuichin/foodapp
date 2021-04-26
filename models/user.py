from models.base_model import BaseModel
import peewee as pw
from playhouse.hybrid import hybrid_property


class User(BaseModel):
    username = pw.CharField(unique=True, null= False)
    email = pw.CharField(unique = True, null= False)
    password_hash = pw.CharField(null= False)
    phone = pw.TextField(null=True)
    payment_info = pw.CharField(null=True)
    image_path = pw.TextField(null=True)
    
    

