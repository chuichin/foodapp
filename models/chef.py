from models.base_model import BaseModel
import peewee as pw

class Chef(BaseModel):
    username = pw.CharField(unique=True, null= False)
    email = pw.CharField(unique = True, null= False)
    password_hash = pw.CharField(null= False)
    password = None  
    chef_photo_url = pw.TextField(null=True)
    bio = pw.TextField(null=False)
    price = pw.IntegerField(null=False)
    payment_info = pw.CharField()

    def calendar():  
        pass

    def overall_rating():
        pass
    #sum up the ratings