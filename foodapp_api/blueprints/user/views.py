import os
from app import app, s3
from flask import Blueprint, Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt_header, create_refresh_token
from models.user import User
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from datetime import timedelta

users_api_blueprint = Blueprint('users_api', __name__)

jwt = JWTManager(app) 

# POST /users/new - sign up as new user
@users_api_blueprint.route("/new", methods = ["POST"])
def user_new():
    # Request: requires username, password, email, payment_info, image_file_path
    if request.content_length == 0:
        return jsonify(message="Nothing is passed, all fields are required!",status="failed"), 400             
    else:
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        email = request.json.get("email", None)
        phone = request.json.get("phone", None)
        image_path = request.json.get("profileImage", None)
        
        if User.get_or_none(User.username == username):
            return jsonify(message="Username already exist", status="failed"), 400
        elif User.get_or_none(User.email == email) :
            return jsonify(message="Email already exist", status="failed"), 400
        else:
            newUser = User(username=username, email=email, password_hash=generate_password_hash(password), phone=phone, image_path=image_path)
            if newUser.save():
                
                newUser = User.get(User.username == username, User.email == email)
                access_token = create_access_token(identity=newUser.username, expires_delta=datetime.timedelta(minutes=60), additional_headers={'type':'User'})
                success_response = [{
                    "message": "Successfully created a user and signed in",
                    "status": "success",
                    "auth_token": access_token,
                    "user": {
                        "id": newUser.id,
                        "username": newUser.username,
                        "email": newUser.email,
                        "phone": newUser.phone,
                        "profileImage": newUser.image_path
                    }
            }]
            return jsonify(success_response), 200

# POST /users/login - login as user
@users_api_blueprint.route("/login", methods = ["POST"])
def user_login():
    if request.content_length == 0:
        return jsonify(message="Nothing is passed to log in", status="Failed"), 400
    else:
        password = request.json.get("password", None)
        email = request.json.get("email", None)
        user = User.get_or_none(User.email == email)
        if user:
            result = check_password_hash(user.password_hash, password)
            access_token = create_access_token(identity=user.username, expires_delta=datetime.timedelta(minutes=60), additional_headers={'type':'User'})
            if result:
                return jsonify({
                    "auth_token": access_token,
                    "message": "successfully signed in",
                    "status": "success",
                    "user": {
                        "id": user.id,
                        "username": user.username,
                        "email": user.email,
                        "phone": user.phone,
                        "profileImage": user.image_path
                    }
                })
            else:
                return jsonify({
                    "message": "Wrong password",
                    "status": "failed"
                }), 400
        else:
            return jsonify({
                "message": "This account doesn't exist",
                "status": "failed"
            }), 400

# Return my profile based on what I login
@users_api_blueprint.route('/me', methods=["GET"])
@jwt_required()
def my_profile():
    # verify_jwt_in_request(optional=False, fresh=True)
    # breakpoint()
    if get_jwt_identity():
        current_user = get_jwt_identity()
        if get_jwt_header()['type'] == 'User':
            user = User.get_or_none(User.username == current_user)
            if user:
                return jsonify({
                    "_id": user.id,
                    "createdAt": user.created_at,
                    "email": user.email,
                    "name": user.username,
                    "phone": user.phone,
                    "profileImage": user.image_path
                }), 200
            else: 
                return jsonify({"message": "This account no longer exists"}), 400
        else:
            return jsonify({
                "message": "This account is a Chef's account"
            }), 400

# GET /users/
@users_api_blueprint.route('/', methods=["GET"])
def all_users():
    if User.select():
        all_users = User.select()
        return jsonify([{
            "profileImage": user.image_path,
            "createdAt": user.created_at,
            "_id": user.id,
            "name" : user.username,
            "email" : user.email,
            "phone": user.phone,
        } for user in all_users]), 200
    else:
        return jsonify(message="No users found", status="failed"), 400

# GET /users/<user_id> 
@users_api_blueprint.route("/<user_id>", methods = ["GET"])
def user_id(user_id):
    user = User.get_or_none(User.id == user_id)
    if user:
        return jsonify({
            "profileImage": user.image_path,
            "createdAt": user.created_at,
            "_id": user.id,
            "name" : user.username,
            "email" : user.email,
            "phone": user.phone,
        })
    else:
        return jsonify({
            "message": "User does not exist",
            "status": "failed"
        }), 400


# Check if username exist
@users_api_blueprint.route('/check/username', methods=["GET"])
def check_username():
    if request.is_json == False:
        return jsonify(message="No username passed", status="Failed"), 400    
    username = request.json.get("username", None)
    if username:
        username_exist = User.get_or_none(User.username == username)
        if username_exist:
            return jsonify(message="Username already exist", username=username), 400
        else: 
            return jsonify(message="Username does not exist, you can use this", username=username), 200
    
# Check if email exist
@users_api_blueprint.route('/check/email', methods=["GET"])
def check_email():
    if request.is_json == False:
        return jsonify(message="No email passed", status="Failed"), 400    
    email = request.json.get("email", None)
    if email:
        email_exist = User.get_or_none(User.email == email)
        if email_exist:
            return jsonify(message="Email already exist", email=email), 400
        else: 
            return jsonify(message="Email does not exist, you can use this", email=email), 200
    else:
        return jsonify(message="Nothing passed in JSON"), 400


#UPDATE users/update/ [JWT]
@users_api_blueprint.route("/update", methods=["PUT"])
@jwt_required()
def update_jwt():
    current_user = get_jwt_identity()
    user = User.get_or_none(User.username==current_user)
    if get_jwt_header()['type'] == 'User':
        params = request.get_json()
        if params:
            params.update({'updated_at': datetime.datetime.now()})
            for each in params:
                update = User.update(params).where(User.id == user.id)
            if update.execute():
                return jsonify({
                    "message": "Successfully updated", 
                    "menu_id": user.id,
                    "updated_at": user.updated_at,
                    "updated_column": [each for each in params]
                })
        elif params == None:
            return jsonify({
                "message": "No fields are passed",
                "status": "failed"
            }), 400
    else:
        return jsonify(message="You are logged in as chef instead of user", status= "failed"), 400

# Update User profile image
@users_api_blueprint.route("/image", methods=["PUT"])
@jwt_required()
def update_image():
    if get_jwt_header()['type'] == "User":
        user = User.get_or_none(User.username == get_jwt_identity())
        if request.content_length == 0:
            return jsonify(message="No images passed", status="failed"), 400
        elif request.files['user_image']:
            file = request.files.get('user_image')
            s3.upload_fileobj(
                file,
                "foodapp-new",
                f"users/{user.id}/{file.filename}",
                ExtraArgs={
                    "ACL": "public-read",
                    "ContentType": file.content_type
                }
            )
            update = User.update({User.image_path:f"https://foodapp-new.s3-ap-southeast-1.amazonaws.com/users/{user.id}/{file.filename}"}).where(User.username == user.username).execute()
            updated_user = User.get(User.id == user.id)
            return jsonify({
                "message": "Successfully updated user's profile image",
                "user_id": updated_user.id,
                "image": updated_user.image_path,
            }), 200
    else:
        return jsonify(message="You are not logged in as User"), 400

# DELETE users/delete/<user_id>  [JWT]
@users_api_blueprint.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_jwt():
    if get_jwt_identity():
        current_user = get_jwt_identity()
        user = User.get_or_none(User.username == current_user)
        if user:
            if user.delete_instance():
                return jsonify({"message": "Successfully deleted this user", "user_id": user.id, "status": "success"}), 200
        else:
            return jsonify({"message": "Unable to delete, user no longer exist", "status": "failed"}), 400
