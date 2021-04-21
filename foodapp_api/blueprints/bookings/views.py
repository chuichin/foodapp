from app import app
from flask import Blueprint, Flask, jsonify, request
from models.booking import Booking

bookings_api_blueprint = Blueprint('bookings_api', __name__)

# GET /bookings/chef/<id> - return all bookings for a chef
@bookings_api_blueprint.route("/chef/<chef_id>", methods = ["GET"])
def chef_bookings(chef_id):
    chef_id = request.json.get("chef_id", None)
    all_bookings = Booking.select().where(Booking.chef == chef_id)
    booking = [{
        "id": booking.id,
        "user_id" : booking.user_id,
        "chef_id" : booking.chef_id,
        "price" : booking.price,
        "booking_date" : booking.booking_date,
        "completed": booking.completed,
        "diet_restrictions": booking.diet_restrictions,
        "address" : booking.address,
        "pax" : booking.pax,
        "lunch" : booking.lunch,
        "menu_type": booking.menu_type,
        
    } for booking in all_bookings]
    return jsonify(booking)

# GET /bookings/user/<id>
@bookings_api_blueprint.route("/user/<user_id>", methods = ["GET"])
def user_bookings(user_id):
    user_id = request.json.get("user_id", None)
    all_bookings = Booking.select().where(Booking.user == user_id)
    booking = [{
        "id": booking.id,
        "user_id" : booking.user_id,
        "chef_id" : booking.chef_id,
        "price" : booking.price,
        "booking_date" : booking.booking_date,
        "completed": booking.completed,
        "diet_restrictions": booking.diet_restrictions,
        "address" : booking.address,
        "pax" : booking.pax,
        "lunch" : booking.lunch,
        "menu_type": booking.menu_type,
        
    } for booking in all_bookings]
    return jsonify(booking)


# GET /bookings/<id> - return specific booking
@bookings_api_blueprint.route("/<id>", methods = ["GET"])
def booking_id(id):
    booking = Booking.get_or_none(Booking.id == id)
    return jsonify({
        "id": booking.id,
        "user_id" : booking.user_id,
        "chef_id" : booking.chef_id,
        "price" : booking.price,
        "booking_date" : booking.booking_date,
        "completed": booking.completed,
        "diet_restrictions": booking.diet_restrictions,
        "address" : booking.address,
        "pax" : booking.pax,
        "lunch" : booking.lunch,
        "menu_type": booking.menu_type,
    })

# POST /bookings/new - submit a booking by user
@bookings_api_blueprint.route("/new", methods = ["POST"])
def booking_new():
# Request require user_id, chef_id, price, booking_date, completed, diet_restrictions etc etc 
    user = request.json.get("user_id", None)
    chef = request.json.get("chef_id", None)
    price = request.json.get("price", None)
    booking_date = request.json.get("booking_date", None)
    completed = request.json.get("completed", None)
    diet_restrictions = request.json.get("diet_restrictions", None)
    address = request.json.get("address", None)
    pax = request.json.get("pax", None)
    lunch = request.json.get("lunch", None)
    menu_type = request.json.get("menu_type", None)
    hob_type = request.json.get("hob_type", None) 
    no_of_hob= request.json.get("no_of_hob", None) 
    cancelled = request.json.get("cancelled", None) 
    payment_type = request.json.get("payment_type", None) 
 
    new_booking = Booking(user=user, chef=chef, price=price, booking_date=booking_date, completed=completed, diet_restrictions=diet_restrictions, address=address, pax=pax, lunch=lunch, menu_type=menu_type, hob_type=hob_type, no_of_hob= no_of_hob,cancelled=cancelled, payment_type=payment_type )
    
    if new_booking.save():
        return jsonify({
            "message": "Successfully created new booking",
            "status": "success"
        }), 200
    else:
        return jsonify({
            "message": "failed to create new booking",
            "status": "failed"
        }), 400
    
