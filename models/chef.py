import peewee as pw
from models.base_model import BaseModel
from playhouse.hybrid import hybrid_property


class Chef(BaseModel):
    username = pw.CharField(unique=True, null= False)
    email = pw.CharField(unique = True, null= False)
    password_hash = pw.CharField(null= False)
    password = None  
    image_path = pw.TextField(null=True)
    bio = pw.TextField(null=False)
    price = pw.IntegerField(null=False)
    payment_info = pw.CharField()

    @hybrid_property
    def calendar():  
        pass

    @hybrid_property
    def overall_rating(self):
        total_rating = sum([review.rating] for review in self.reviews.select().where(self.reviews == id))
        return total_rating

    @hybrid_property
    def image():
        pass
    #get the photo url ~