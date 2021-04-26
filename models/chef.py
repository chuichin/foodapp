import peewee as pw
from models.base_model import BaseModel
from playhouse.hybrid import hybrid_property



class Chef(BaseModel):
    username = pw.CharField(unique=True, null= False)
    email = pw.CharField(unique = True, null= False)
    password_hash = pw.CharField(null= False)
    phone = pw.TextField(null=True)
    bio = pw.TextField(null=True)
    price = pw.IntegerField(null=True)
    payment_info = pw.CharField(null=True)
    image_path = pw.TextField(null=True)

    @hybrid_property
    def calendar(input):  
        return "TBC"

    @hybrid_property
    def overall_rating(self):
        from models.review import Review
        ratings = [each.rating for each in Review.select().where(Review.chef_id == self.id)]
        if len(ratings) == 0:
            return 0
        else: 
            average_rating =sum(ratings)/len(ratings)
            return average_rating




