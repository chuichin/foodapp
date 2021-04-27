from models.base_model import BaseModel
from models.user import User
from models.chef import Chef
import datetime
import peewee as pw

class Booking(BaseModel):
    user = pw.ForeignKeyField(User, backref="bookings", on_delete="CASCADE")
    chef = pw.ForeignKeyField(Chef, backref="bookings", on_delete="CASCADE")
    address = pw.CharField(null=True)
    service_type = pw.TextField(null=True)
    pax = pw.TextField(null=True)
    meal_type = pw.TextField(null=True) #lunch/dinner
    menu_type = pw.TextField(null=True) #based on category
    hob_type = pw.CharField(null=True)
    no_of_hob = pw.IntegerField(null=True)
    oven = pw.BooleanField(null=True)
    price = pw.FloatField(null=True)
    diet_restrictions= pw.TextField(null=True)
    proposed_date = pw.DateField(null=True)
    message = pw.TextField(null=True)
    completed = pw.BooleanField(default=False)
    payment_status = pw.CharField(default=False)
    confirmed = pw.BooleanField(default=False) 
    cancelled = pw.BooleanField(default=False)
    active = pw.BooleanField(default=False)
