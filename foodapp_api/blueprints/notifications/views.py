import os
from app import app, s3
from flask import Blueprint, Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt_header
from models.user import User
from models.chef import Chef
from models.booking import Booking


notifications_api_blueprint = Blueprint('notifications_api', __name__)

jwt = JWTManager(app) 

# GET /notifications/new-bookings [new orders for Chef or new orders created by User but pending]
@notifications_api_blueprint.route('/new-bookings/', methods=["GET"])
@jwt_required()
def new_bookings():
    # returns new bookings for Chef
    if get_jwt_header()['type'] == "Chef":
        current_chef = Chef.get_or_none(Chef.username == get_jwt_identity())
        bookings = Booking.select().where(Booking.chef_id == current_chef.id, Booking.active == True, Booking.confirmed == False)
        if bookings:
            return jsonify({
                "count": bookings.count(),
                "results": [{
                    # not complete information
                    "booking_id": booking.id,
                    "user_id": booking.user_id,
                    "chef_id": booking.chef_id,
                    "price": booking.price,
                    "proposed_date": booking.proposed_date,
                    "booking_completed": booking.completed,
                    "booking_confirmed": booking.confirmed,
                    "booking_active": booking.active,
                } for booking in bookings]
            })
        else:
            return jsonify({
                "message": "There are no new bookings for this chef",
                "status": "Failed"
            }), 400
     # Returns pending bookings for User
    else:
        current_user = User.get_or_none(User.username == get_jwt_identity())
        bookings = Booking.select().where(Booking.user_id == current_user.id, Booking.active == True, Booking.confirmed == False)
        if bookings:
            return jsonify({
                "count": bookings.count(),
                "results": [{
                # not complete information
                "booking_id": booking.id,
                "user_id": booking.user_id,
                "chef_id": booking.chef_id,
                "price": booking.price,
                "proposed_date": booking.proposed_date,
                "booking_completed": booking.completed,
                "booking_confirmed": booking.confirmed,
                "booking_active": booking.active,
            } for booking in bookings]
            })
        else:
            return jsonify({
                "message": "There are no new bookings created by this user",
                "status": "Failed"
            }), 400



# GET /notifications/approved-bookings [approved bookings for Chef]
@notifications_api_blueprint.route('/approved-bookings/', methods=["GET"])
@jwt_required()
def approved_bookings():
    # Returns approved orders by Chef
    if get_jwt_header()['type'] == "Chef":
        current_chef = Chef.get_or_none(Chef.username == get_jwt_identity())
        bookings = Booking.select().where(Booking.chef_id == current_chef.id, Booking.active == True, Booking.confirmed == True)
        if bookings:
            return jsonify({
                "count": bookings.count(),
                "results": [{
                    # not complete information
                    "booking_id": booking.id,
                    "user_id": booking.user_id,
                    "chef_id": booking.chef_id,
                    "price": booking.price,
                    "proposed_date": booking.proposed_date,
                    "booking_completed": booking.completed,
                    "booking_confirmed": booking.confirmed,
                    "booking_active": booking.active,
                } for booking in bookings]
            })
        else:
            return jsonify({
                "message": "There are no confirmed bookings for this chef",
                "status": "Failed"
            }), 400
    # Returns confirmed bookings for User
    else:
        current_user = User.get_or_none(User.username == get_jwt_identity())
        bookings = Booking.select().where(Booking.user_id == current_user.id, Booking.active == True, Booking.confirmed == True)
        if bookings:
            return jsonify({
                "count": bookings.count(),
                "results": [{
                # not complete information
                "booking_id": booking.id,
                "user_id": booking.user_id,
                "chef_id": booking.chef_id,
                "price": booking.price,
                "proposed_date": booking.proposed_date,
                "booking_completed": booking.completed,
                "booking_confirmed": booking.confirmed,
                "booking_active": booking.active,
            } for booking in bookings]
            })
        else:
            return jsonify({
                "message": "There are no confirmed bookings for this user",
                "status": "Failed"
            }), 400


# GET /notifications/rejected-bookings (active = False, cancelled = False)
@notifications_api_blueprint.route('/rejected-bookings/', methods=["GET"])
@jwt_required()
def rejected_bookings():
    if get_jwt_header()['type'] == "Chef":
        current_chef = Chef.get_or_none(Chef.username == get_jwt_identity())
        bookings = Booking.select().where(Booking.chef_id == current_chef.id, Booking.active == False, Booking.cancelled == False)
        if bookings:
            return jsonify({
                "count": bookings.count(),
                "results": [{
                    # not complete information
                    "booking_id": booking.id,
                    "user_id": booking.user_id,
                    "chef_id": booking.chef_id,
                    "price": booking.price,
                    "proposed_date": booking.proposed_date,
                    "booking_completed": booking.completed,
                    "booking_confirmed": booking.confirmed,
                    "booking_active": booking.active,
                } for booking in bookings]
            })
        else:
            return jsonify({
                "message": "There are no rejected bookings for this chef",
                "status": "Failed"
            }), 400
    # Returns confirmed bookings for User
    else:
        current_user = User.get_or_none(User.username == get_jwt_identity())
        bookings = Booking.select().where(Booking.user_id == current_user.id, Booking.active == False, Booking.confirmed == False)
        if bookings:
            return jsonify({
                "count": bookings.count(),
                "results": [{
                # not complete information
                "booking_id": booking.id,
                "user_id": booking.user_id,
                "chef_id": booking.chef_id,
                "price": booking.price,
                "proposed_date": booking.proposed_date,
                "booking_completed": booking.completed,
                "booking_confirmed": booking.confirmed,
                "booking_active": booking.active,
            } for booking in bookings]
            })
        else:
            return jsonify({
                "message": "There are no rejected bookings for this user",
                "status": "Failed"
            }), 400

# GET /notifications/cancelled-bookings
@notifications_api_blueprint.route('/cancelled-bookings/', methods=["GET"])
@jwt_required()
def cancelled_bookings():
    # Returns approved orders by Chef
    if get_jwt_header()['type'] == "Chef":
        current_chef = Chef.get_or_none(Chef.username == get_jwt_identity())
        bookings = Booking.select().where(Booking.chef_id == current_chef.id, Booking.active == False, Booking.confirmed == True, Booking.cancelled == True)
        if bookings:
            return jsonify({
                "count": bookings.count(),
                "results": [{
                    # not complete information
                    "booking_id": booking.id,
                    "user_id": booking.user_id,
                    "chef_id": booking.chef_id,
                    "price": booking.price,
                    "proposed_date": booking.proposed_date,
                    "booking_completed": booking.completed,
                    "booking_confirmed": booking.confirmed,
                    "booking_active": booking.active,
                } for booking in bookings]
            })
        else:
            return jsonify({
                "message": "There are no cancelled bookings for this chef",
                "status": "Failed"
            }), 400
    # Returns confirmed bookings for User
    else:
        current_user = User.get_or_none(User.username == get_jwt_identity())
        bookings = Booking.select().where(Booking.user_id == current_user.id, Booking.active == False, Booking.confirmed == True, Booking.cancelled == True)
        if bookings:
            return jsonify({
                "count": bookings.count(),
                "results": [{
                # not complete information
                "booking_id": booking.id,
                "user_id": booking.user_id,
                "chef_id": booking.chef_id,
                "price": booking.price,
                "proposed_date": booking.proposed_date,
                "booking_completed": booking.completed,
                "booking_confirmed": booking.confirmed,
                "booking_active": booking.active,
            } for booking in bookings]
            })
        else:
            return jsonify({
                "message": "There are no cancelled bookings for this user",
                "status": "Failed"
            }), 400

