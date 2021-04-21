import os
from app import app, s3
from flask import Blueprint, Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from models.chef import Chef
from werkzeug.security import check_password_hash, generate_password_hash

chefs_api_blueprint = Blueprint('chefs_api',
                                __name__)

# jwt = JWTManager(app) #not sure if needed yet

# GET /chefs/all - return list of chefs and details
@chefs_api_blueprint.route('/all', methods=["GET"])
def index():
    chefs = Chef.select()
    if chefs:
        all_chefs = [{
            "id": chef.id,
            "username": chef.username,
            "email": chef.email,
            # "password": chef.password_hash,
            "image": chef.image_path,
            "bio": chef.bio,
            "price": chef.price,
            "payment_info": chef.payment_info,
            "rating": chef.overall_rating,
            "calendar": chef.calendar
        } for chef in chefs]
        return jsonify(all_chefs), 200
    else:
        return jsonify({
            "message": "There are no chefs created yet"
        })

# POST /chefs/new  - to sign up as new chef
@chefs_api_blueprint.route('/new', methods=["POST"])
def chef_new():
# Request: requires username, password, email, bio, price, payment_info, image_file_path
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    email = request.json.get("email", None)
    bio = request.json.get("bio", None)
    price = request.json.get("price", None)
    payment_info = request.json.get("payment_info", None)
    image_path = request.json.get("image", None)

    if username==None or email==None or password==None:
        return jsonify({
            "message": [
                "All fields are required!"
            ],
            "status": "failed"
            }), 400 
    elif Chef.get_or_none(Chef.username == username) or Chef.get_or_none(Chef.email == email):
        return jsonify({
            "message": [
                "Email is already in use",
                "Username is already in use"
            ],
            "status": "failed"
            }), 400      
    else:
        newChef = Chef(username=username, email=email, password_hash=generate_password_hash(password), image_path=image_path, bio=bio, price=price,payment_info=payment_info)
        if newChef.save():
            access_token = create_access_token(identity=username)
            success_response = [{
                "message": "Successfully created a user and signed in",
                "status": "success",
                "user": {
                    "id":1,
                    "username":username,
                    "profile_picture":"NA for now"
                    # return other info as well 
                }
            }]
            return jsonify(success_response), 200
        else:
            return jsonify({
                "message": "Failed to sign up for this user, please try again"
            }), 400



# POST /chefs/login - to allow chef login
@chefs_api_blueprint.route('/login', methods=["POST"])
def chef_login():
# Request requires username, password 
    username = request.json.get("username", None)
    password = request.json.get("password", None)
    email = request.json.get("email", None)
    chef = Chef.get_or_none(Chef.email == email)
    if chef:
        result = check_password_hash(chef.password_hash, password)
        access_token = create_access_token(identity=username)
        if result:
            return jsonify({
                "auth-token": access_token,
                "message": "successfully signed in",
                "status": "success",
                "chef": {
                    "id": 1,
                    "username": chef.username
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


# GET /chefs/<id> - to return chef profile
@chefs_api_blueprint.route('/<id>', methods=["GET"])
def chef_id(id):
    chef = Chef.get_or_none(Chef.id == id)
    if chef:
        return jsonify({
            "id": chef.id,
            "username" : chef.username,
            "email" : chef.email,
            "bio" : chef.bio,
            "price" : chef.price,
            "payment_info" : chef.payment_info,
            "image_path": chef.image_path
        })
    else:
        return jsonify({
            "message": "User does not exist",
            "status": "failed"
        }), 400

# POST /chef/<id>/profile_image - uploading profile image
@chefs_api_blueprint.route("/<id>/profile_image", methods=["POST"])
def profile_image(id):
    chef = Chef.get_or_none(Chef.id == id)
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
        chef.image_path = f"https://{os.getenv('S3_BUCKET')}.s3-ap-southeast-1.amazonaws.com/{file.filename}"
        if chef.save():
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

