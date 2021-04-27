from app import app
from flask import Blueprint, Flask, jsonify, request
from models.booking import Booking
from models.chef import Chef
from models.user import User
import datetime
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt_header


bookings_api_blueprint = Blueprint('bookings_api', __name__)

jwt = JWTManager(app) 

# POST /bookings/new - submit a booking by user  (active = True)
@bookings_api_blueprint.route("/new", methods = ["POST"])
@jwt_required()
def booking_new():
    current_user = get_jwt_identity()
    if get_jwt_header()['type'] == "User":
        response = request.get_json()
        user = User.get_or_none(User.email == current_user)

        new_booking = Booking(user=user.id, chef=response['chef'], address=response['address'], service_type=response['service_type'], pax=response['pax'], meal_type=response['meal_type'], menu_type=response['menu_type'], hob_type=response['hob_type'], no_of_hob=response['no_of_hob'], oven=response['oven'], price=response['price'], diet_restrictions=response['diet_restrictions'], proposed_date=response['proposed_date'], message=response['message'], completed=False, payment_status=False, confirmed=False, active=True, cancelled=False)
        if new_booking.save():
            return jsonify({
                "message": "Successfully created new booking",
                "status": "success",
                "booking_id": new_booking.id,
                "chef_id": new_booking.chef_id,
                "user_id": new_booking.user_id,
                "completed":new_booking.completed,
                "payment_status":new_booking.payment_status,
                "confirmed":new_booking.confirmed,
                "active":new_booking.active,
                "cancelled":new_booking.cancelled
            }), 200
        else:
            return jsonify({
                "message": "failed to create new booking",
                "status": "failed"
            }), 400
    else:
        return jsonify(message="You are logged in as Chef, not User ", status="success"), 400

# GET /bookings/chef/<chef_id> - return all bookings for a chef
@bookings_api_blueprint.route("/chef/<chef_id>", methods = ["GET"])
def chef_bookings(chef_id):
    existing_chef = Chef.get_or_none(Chef.id == chef_id)
    if existing_chef:
        all_bookings = Booking.select().where(Booking.chef == chef_id)
        if all_bookings:
            booking = {
                "status": "success",
                "booking_id": booking.id,
                "count": all_bookings.count(),
                "results": [{
                    "user": booking.user_id,
                    "chef": booking.chef_id,
                    "address": booking.address,
                    "service_type": booking.service_type,
                    "pax": booking.pax,
                    "meal_type": booking.meal_type,
                    "menu_type": booking.menu_type,
                    "hob_type": booking.hob_type,
                    "no_of_hob": booking.no_of_hob,
                    "oven": booking.oven,
                    "price": booking.price,
                    "diet_restrictions": booking.diet_restrictions, 
                    "proposed_date": booking.proposed_date,
                    "message": booking.message,
                    "completed": booking.completed,
                    "payment_status": booking.payment_status,
                    "confirmed": booking.confirmed,
                    "active": booking.active,
                    "cancelled": booking.cancelled
                } for booking in all_bookings]
            }
            return jsonify(booking), 200
        else:
            return jsonify({"results": []}), 200
    else:
        return jsonify({
            "message": "This chef does not exist",
            "status": "Failed"
        }), 400


# GET /bookings/user/<id>
@bookings_api_blueprint.route("/user/<user_id>", methods = ["GET"])
def user_bookings(user_id):
    existing_user = User.get_or_none(User.id == user_id)
    if existing_user:
        all_bookings = Booking.select().where(Booking.user == user_id)
        if all_bookings:
            booking = {
                "status": "success",
                "booking_id": booking.id,
                "count": all_bookings.count(),
                "results": [{
                    "user": booking.user_id,
                    "chef": booking.chef_id,
                    "address": booking.address,
                    "service_type": booking.service_type,
                    "pax": booking.pax,
                    "meal_type": booking.meal_type,
                    "menu_type": booking.menu_type,
                    "hob_type": booking.hob_type,
                    "no_of_hob": booking.no_of_hob,
                    "oven": booking.oven,
                    "price": booking.price,
                    "diet_restrictions": booking.diet_restrictions, 
                    "proposed_date": booking.proposed_date,
                    "message": booking.message,
                    "completed": booking.completed,
                    "payment_status": booking.payment_status,
                    "confirmed": booking.confirmed,
                    "active": booking.active,
                    "cancelled": booking.cancelled
                } for booking in all_bookings]
            }
            return jsonify(booking), 200
        else:
            return jsonify({"results": []}), 200
    else:
        return jsonify({
            "message": "This user does not not exist",
            "status": "failed"
        }), 400

    
# GET /bookings/<id> - return specific booking
@bookings_api_blueprint.route("/<booking_id>", methods = ["GET"])
def booking_id(booking_id):
    booking = Booking.get_or_none(Booking.id == booking_id)
    if booking:
        return jsonify({
            "booking_id": booking.id,
            "user": booking.user_id,
            "chef": booking.chef_id,
            "address": booking.address,
            "service_type": booking.service_type,
            "pax": booking.pax,
            "meal_type": booking.meal_type,
            "menu_type": booking.menu_type,
            "hob_type": booking.hob_type,
            "no_of_hob": booking.no_of_hob,
            "oven": booking.oven,
            "price": booking.price,
            "diet_restrictions": booking.diet_restrictions, 
            "proposed_date": booking.proposed_date,
            "message": booking.message,
            "completed": booking.completed,
            "payment_status": booking.payment_status,
            "confirmed": booking.confirmed,
            "active": booking.active,
            "cancelled": booking.cancelled
            
        }), 200
    else: 
        return jsonify({
            "message": "This booking does not exist",
            "status": "Failed"
        }), 400


# UPDATE /bookings/update/<booking_id>
@bookings_api_blueprint.route('/update/<booking_id>', methods=["PUT"] )
@jwt_required()
def update(booking_id):
    booking = Booking.get_or_none(Booking.id==booking_id)
    params = request.get_json()
    current_user = get_jwt_identity()
    if get_jwt_header()['type'] != "User":
        return jsonify(message="You are logged in as Chef, not user. Only user can edit booking.", status="success"), 400
    else:
        if booking and params:
            params.update({'updated_at': datetime.datetime.now()})
            for each in params:
                update = Booking.update(params).where(Booking.id == booking_id)
            if update.execute():
                return jsonify({
                    "message": "Successfully updated", 
                    "booking_id": booking.id,
                    "updated_at": booking.updated_at,
                    "updated_column": [each for each in params],
                    "completed": booking.completed,
                    "payment_status": booking.payment_status,
                    "confirmed": booking.confirmed,
                    "active": booking.active,
                    "cancelled": booking.cancelled
                })
            else:
                return jsonify({
                    "message": "Unable to update, please try again",
                    "status": "failed"
                }), 400
        elif booking == None:
            return jsonify({
                "message": "This booking doesn't exist",
                "status": "failed"
            }),400
        elif params == None:
            return jsonify({
                "message": "No fields are passed",
                "status": "failed"
            }), 400

# DELETE /bookings/delete/<booking_id>
@bookings_api_blueprint.route("/delete/<booking_id>", methods=["DELETE"])
def delete(booking_id):
    booking = Booking.get_or_none(Booking.id == booking_id)
    if booking:
        if booking.delete_instance():
            return jsonify({"message": "Successfully deleted", "booking_id": booking_id, "status": "success"}), 200
        else:
            return jsonify({"message": "Unable to delete", "status": "failed"}), 400
    else: 
        return jsonify({"message": "Unable to find this booking", "status": "failed"}), 400

# Chef approves booking (confirmed=True(update this), active=True)
@bookings_api_blueprint.route("/chef-approve/<booking_id>", methods=["PUT"])
@jwt_required()
def chef_approve(booking_id):
    if get_jwt_header()['type'] == "Chef":
        current_chef = Chef.get_or_none(Chef.email == get_jwt_identity())
        booking = Booking.get_or_none(Booking.id == booking_id)
        if booking:
            if booking.chef_id == current_chef.id:
                booking.confirmed = True
                if booking.save():
                    return jsonify({
                        "booking_id": booking_id,
                        "completed": booking.completed,
                        "payment_status": booking.payment_status,
                        "confirmed": booking.confirmed,
                        "active": booking.active,
                        "cancelled": booking.cancelled,
                        "status": "success"
                    }), 200
            else:
                return jsonify({
                    "message": "You are logged in as another chef",
                    "booking_chef_id": booking.chef_id,
                    "status": "failed"
                }), 400
        else:
            return jsonify({
                "message": "Booking does not exist",
                "status": "Failed"
            }), 400
    else:
        return jsonify({
            "message": "You have to log in as Chef, not user",
            "status": "Failed"
        }), 400

# Chef rejects booking (confirmed=False (default), active=False(update this))
@bookings_api_blueprint.route("/chef-reject/<booking_id>", methods=["PUT"])
@jwt_required()
def chef_reject(booking_id):
    if get_jwt_header()['type'] == "Chef":
        current_chef = Chef.get_or_none(Chef.email == get_jwt_identity())
        booking = Booking.get_or_none(Booking.id == booking_id)
        if booking:
            if booking.chef_id == current_chef.id:
                booking.active = False
                if booking.save():
                    return jsonify({
                        "booking_id": booking_id,
                        "completed": booking.completed,
                        "payment_status": booking.payment_status,
                        "confirmed": booking.confirmed,
                        "active": booking.active,
                        "cancelled": booking.cancelled,
                        "status": "success"
                    }), 200
                else:
                    return jsonify({
                        "message": "Unable to reject booking", 
                        "status": "Failed"
                    }), 400
            else:
                return jsonify({
                    "message": "You are logged in as another chef",
                    "booking_chef_id": booking.chef_id,
                    "status": "failed"
                }), 400
        else:
            return jsonify({
                "message": "Booking does not exist",
                "status": "Failed"
            }), 400
    else:
        return jsonify({
            "message": "You have to log in as Chef, not user",
            "status": "Failed"
        }), 400


# User cancels booking after chef approves (confirmed=True, active=False(update this), cancelled=True(update this))
@bookings_api_blueprint.route("/user-cancel/<booking_id>", methods=["PUT"])
@jwt_required()
def user_cancel(booking_id):
    if get_jwt_header()['type'] == "User":
        current_user = User.get_or_none(User.email == get_jwt_identity())
        booking = Booking.get_or_none(Booking.id == booking_id)
        if booking:
            if booking.user_id == current_user.id:
                booking.active = False
                booking.cancelled = True
                if booking.save():
                    return jsonify({
                        "booking_id": booking_id,
                        "completed": booking.completed,
                        "payment_status": booking.payment_status,
                        "confirmed": booking.confirmed,
                        "active": booking.active,
                        "cancelled": booking.cancelled,
                        "status": "success"
                    }), 200
                else:
                    return jsonify({
                        "message": "Unable to cancel booking", 
                        "status": "Failed"
                    }), 400
            else:
                return jsonify({
                    "message": "You are logged in as another user",
                    "booking_chef_id": booking.chef_id,
                    "status": "failed"
                }), 400
        else:
            return jsonify({
                "message": "Booking does not exist",
                "status": "Failed"
            }), 400
    else:
        return jsonify({
            "message": "You have to log in as User, not Chef",
            "status": "Failed"
        }), 400