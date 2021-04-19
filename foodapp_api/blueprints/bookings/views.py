from app import app
from flask import Blueprint, Flask, jsonify, request
from models.booking import Booking

bookings_api_blueprint = Blueprint('bookings_api', __name__)

# GET /booking/chef/<id> - return all bookings for a chef
@bookings_api_blueprint.route("/chef/<chef_id>", methods = ["GET"])
def bookings(chef_id):
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

# GET /booking/user/<id>
@bookings_api_blueprint.route("/user/<user_id>", methods = ["GET"])
def bookings(user_id):
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


# GET /booking/<id> - return specific booking
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

# POST /booking/new - submit a booking by user
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

    new_booking = Booking(user=user, chef=chef, price=price, booking_date=booking_date, completed=completed, diet_restrictions=diet_restrictions, address=address, pax=pax, lunch=lunch, menu_type=menu_type)
    
    if new_booking.save():
        return jsonify({
            "message": "Successfully created new booking",
            "status": "success"
        }), 200
    else:
        return jsonify({
            "message": "failed to create new booking",
            "status": "success"
        })
    
