from models.base_model import BaseModel
import peewee as pw
from playhouse.hybrid import hybrid_property


class User(BaseModel):
    username = pw.CharField(unique=True, null= False)
    email = pw.CharField(unique = True, null= False)
    password_hash = pw.CharField(null= False)
    password = None
    payment_info = pw.CharField()
    image_path = pw.TextField(null=True)
    
    @hybrid_property
    def profile_picture(input):
        pass

    

