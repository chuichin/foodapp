import os
from app import app, s3
from flask import Blueprint, Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from models.user import User
from werkzeug.security import check_password_hash


users_api_blueprint = Blueprint('users_api', __name__)

jwt = JWTManager(app) #not sure if needed yet

# POST /user/new - sign up as new user
@users_api_blueprint.route("/new", methods = ["POST"])
def user_new():
    # Request: requires username, password, email, payment_info, image_file_path
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    email = request.json.get("email", None)
    payment_info = request.json.get("payment_info", None)
    image_path = request.json.get("image", None)

    if User.get_or_none(User.username == username) or User.get_or_none(User.email == email):
        return jsonify({
            "message": [
                "Email is already in use",
                "Username is already in use"
            ],
            "status": "failed"
            }), 400
    elif username==None or email==None or password==None:
        return jsonify({
            "message": [
                "All fields are required!"
            ],
            "status": "failed"
            }), 400                
    else:
        access_token = create_access_token(identity=username)
        # to create new Chef database using the data from above
        # if successfully created, then move to success_response
        # need to maybe create sth to upload to Amazon?
        success_response = [{
            "auth_token": access_token,
            "message": "Successfully created a user and signed in",
            "status": "success",
            "user": {
                "id":1,
                "username":username,
                "profile_picture":"NA for now"
                # return other info as well 
            }
        }]
        return jsonify(success_response)

# POST /users/login - login as user
@users_api_blueprint.route("/login", methods = ["POST"])
def user_login():
    # Request requires username, password 
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    email = request.json.get("email", None)
    user = User.get_or_none(User.email == email)
    if user:
        result = check_password_hash(user.password_hash, password)
        access_token = create_access_token(identity=username)
        if result:
            return jsonify({
                "auth-token": "super long kjdsfkjdslfs",
                "message": "successfully signed in",
                "status": "success",
                "user": {
                    "id": 1,
                    "username": user.username
                }
            })
        else:
            return jsonify({
                "message": "Wrong password",
                "status": "fail"
            }), 400
    else:
        return jsonify({
            "message": "This account doesn't exist",
            "status": "fail"
        }), 400


@users_api_blueprint.route("/<id>", methods = ["GET"])
def user_id(id):
    user = User.get_or_none(User.id == id)
    if user:
        return jsonify({
            "id": user.id,
            "username" : user.username,
            "email" : user.email,
            "payment_info" : user.payment_info,
            "image_path": user.image_path
        })
    else:
        return jsonify({
            "message": "User does not exist",
            "status": "failed"
        }), 400

# POST /users/<id>/profile_image - uploading profile image
@users_api_blueprint.route("/<id>/profile_image", methods=["POST"])
def profile_image(id):
    user = User.get_or_none(User.id == id)
    if request.files["image_upload"]:
        file = request.files.get("image_upload")
        s3.upload_fileobj(
            file,
            # need to set .env
            os.getenv("S3_BUCKET"),
            file.filename,
            ExtraArgs={
                "ACL": "public-read",
                "ContentType": file.content_type
            })
            # need to set .env
        user.image_path = f"https://{os.getenv('S3_BUCKET')}.s3-ap-southeast-1.amazonaws.com/{file.filename}"
        if user.save():
            return jsonify({
                "message": "Profile image successfully uploaded"
            })
        else:
            return jsonify({
                "message":"Error in uploading profile image"
            }), 400
    else:
        return jsonify({
            "message":"Error in uploading profile image"
        }), 400


