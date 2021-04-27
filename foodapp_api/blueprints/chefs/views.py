import os
from app import app, s3
from flask import Blueprint, Flask, jsonify, request
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, get_jwt_header
from models.chef import Chef
from werkzeug.security import check_password_hash, generate_password_hash
import datetime
from datetime import timedelta

chefs_api_blueprint = Blueprint('chefs_api',
                                __name__)

jwt = JWTManager(app) #not sure if needed yet

# POST /chefs/new  - to sign up as new chef
@chefs_api_blueprint.route('/new', methods=["POST"])
def chef_new():
    if request.content_length == 0:
        return jsonify(message="Nothing is passed, all fields are required!",status="failed"), 400             
    else:
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        email = request.json.get("email", None)
        phone = request.json.get("phone", None)
        image_path = request.json.get("profileImage", None)
        
        if Chef.get_or_none(Chef.username == username):
            return jsonify(message="Username already exist", status="failed"), 400
        elif Chef.get_or_none(Chef.email == email) :
            return jsonify(message="Email already exist", status="failed"), 400
        else:
            newChef = Chef(username=username, email=email, password_hash=generate_password_hash(password), phone=phone, image_path=image_path)
            if newChef.save():
                
                newChef = Chef.get(Chef.username == username, Chef.email == email)
                access_token = create_access_token(identity=newChef.email, expires_delta=datetime.timedelta(minutes=60), additional_headers={'type':'Chef'})
                success_response = [{
                    "message": "Successfully created a user and signed in",
                    "status": "success",
                    "auth_token": access_token,
                    "user": {
                        "id": newChef.id,
                        "username": newChef.username,
                        "email": newChef.email,
                        "phone": newChef.phone,
                        "profileImage": newChef.image_path
                    }
            }]
            return jsonify(success_response), 200



# POST /chefs/login - to allow chef login
@chefs_api_blueprint.route('/login', methods=["POST"])
def chef_login():
    if request.content_length == 0:
        return jsonify(message="Nothing is passed to log in", status="Failed"), 400
    else:
        password = request.json.get("password", None)
        email = request.json.get("email", None)
        chef = Chef.get_or_none(Chef.email == email)
        if chef:
            result = check_password_hash(chef.password_hash, password)
            access_token = create_access_token(identity=chef.email, expires_delta=datetime.timedelta(minutes=60), additional_headers={'type':'Chef'})
            if result:
                return jsonify({
                    "auth_token": access_token,
                    "message": "successfully signed in",
                    "status": "success",
                    "user": {
                        "id": chef.id,
                        "username": chef.username,
                        "email": chef.email,
                        "phone": chef.phone,
                        "profileImage": chef.image_path
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


# GET /chefs/ - return list of chefs and details
@chefs_api_blueprint.route('/', methods=["GET"])
def index():
    chefs = Chef.select()
    if chefs:
        all_chefs = {
            "_status": "success",
            "_no_of_chefs": chefs.count(),
            "results": [{
                "profileImage": chef.image_path,
                "ratingAverage": chef.overall_rating,
                "createdAt": chef.created_at,
                "_id": chef.id,
                "name": chef.username,
                "email": chef.email,
                "phone": chef.phone
            } for chef in chefs]
        }
        return jsonify(all_chefs), 200
    else:
        return jsonify({"results": []}), 200



# GET /chefs/<id> - to return chef profile
@chefs_api_blueprint.route('/<id>', methods=["GET"])
def chef_id(id):
    chef = Chef.get_or_none(Chef.id == id)
    if chef:
        chef_profile = {
            "_status": "success",
            "chef_profile": {
                "profileImage": chef.image_path,
                "ratingAverage": chef.overall_rating,
                "createdAt": chef.created_at,
                "_id": chef.id,
                "name": chef.username,
                "email": chef.email,
                "phone": chef.phone
        }}
        return jsonify(chef_profile)
    else:
        return jsonify({
            "message": "User does not exist",
            "status": "failed"
        }), 400



# UPDATE /chefs/update/<chef_id> [JWT]
@chefs_api_blueprint.route("/update", methods=["PUT"])
@jwt_required()
def update():
    current_chef = get_jwt_identity()
    chef = Chef.get_or_none(Chef.email==current_chef)
    if get_jwt_header()['type'] == 'Chef':
        params = request.get_json()
        if params:
            params.update({'updated_at': datetime.datetime.now()})
            for each in params:
                update = Chef.update(params).where(Chef.id == chef.id)
            if update.execute():
                return jsonify({
                    "message": "Successfully updated", 
                    "menu_id": chef.id,
                    "updated_at": chef.updated_at,
                    "updated_column": [each for each in params]
                })
        elif params == None:
            return jsonify({
                "message": "No fields are passed",
                "status": "failed"
            }), 400
    else:
        return jsonify(message="You are logged in as user instead of chef", status= "failed"), 400

# Return chef's profile based on what I login
@chefs_api_blueprint.route('/me', methods=["GET"])
@jwt_required()
def my_profile():
    if get_jwt_identity():
        current_chef = get_jwt_identity()
        if get_jwt_header()['type'] == 'Chef':
            chef = Chef.get_or_none(Chef.email == current_chef)
            if chef:
                return jsonify({
                    "_id": chef.id,
                    "createdAt": chef.created_at,
                    "email": chef.email,
                    "name": chef.username,
                    "phone": chef.phone,
                    "profileImage": chef.image_path,
                    "bio": chef.bio,
                    "price": chef.price,
                    "payment_info": chef.payment_info
                }), 200
        else: 
            return jsonify({"message": "You are logged in as chef, not user"}), 400
    else:
        return jsonify({
            "message": "User does not exist"
        }), 400


# Update Chef profile image
@chefs_api_blueprint.route("/image", methods=["PUT"])
@jwt_required()
def update_image():
    if get_jwt_header()['type'] == "Chef":
        chef = Chef.get_or_none(Chef.email == get_jwt_identity())
        if request.content_length == 0:
            return jsonify(message="No images passed", status="failed"), 400
        elif request.files['chef_image']:
            file = request.files.get('chef_image')
            s3.upload_fileobj(
                file,
                "foodapp-new",
                f"chefs/{chef.id}/{file.filename}",
                ExtraArgs={
                    "ACL": "public-read",
                    "ContentType": file.content_type
                }
            )
            update = Chef.update({Chef.image_path:f"https://foodapp-new.s3-ap-southeast-1.amazonaws.com/chefs/{chef.id}/{file.filename}"}).where(Chef.username == chef.username).execute()
            updated_chef = Chef.get(Chef.id == chef.id)
            return jsonify({
                "message": "Successfully updated chefs's profile image",
                "user_id": updated_chef.id,
                "image": updated_chef.image_path,
            }), 200
    else:
        return jsonify(message="You are not logged in as Chef"), 400


# DELETE /chefs/delete/<chef_id>
@chefs_api_blueprint.route("/delete", methods=["DELETE"])
@jwt_required()
def delete_jwt():
    if get_jwt_identity():
        current_chef = get_jwt_identity()
        chef = Chef.get_or_none(Chef.email == current_chef)
        if chef:
            if chef.delete_instance():
                return jsonify({"message": "Successfully deleted this chef", "chef_id": chef.id, "status": "success"}), 200
        else:
            return jsonify({"message": "Unable to delete, chef no longer exist", "status": "failed"}), 400

