from models.base_model import BaseModel
from models.user import User
from models.chef import Chef
import datetime
import peewee as pw

class Booking(BaseModel):
    user = pw.ForeignKeyField(User, backref="bookings", on_delete="CASCADE")
    chef = pw.ForeignKeyField(Chef, backref="bookings", on_delete="CASCADE")
    price = pw.FloatField(null=False)
    booking_date = pw.DateField(null=False)
    completed = pw.BooleanField(default=False)
    diet_restrictions = pw.TextField(null=True)
    address = pw.CharField(null=False)
    pax = pw.IntegerField(null=False)
    lunch = pw.BooleanField(default=True) #False means it's dinner
    menu_type = pw.TextField(null=False)
    hob_type = pw.CharField(null=True)
    no_of_hob = pw.IntegerField(null=False)
    cancelled = pw.BooleanField(default=False)
    payment_status = pw.CharField(default=False) #False means not paid
    confirmation_status = pw.CharField(default=False) #True when chef accept booking
