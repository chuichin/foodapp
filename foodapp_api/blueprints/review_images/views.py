import os
from app import app, s3
from flask import Blueprint, Flask, jsonify, request
from models.review_image import ReviewImage
from models.review import Review
from models.user import User
from models.chef import Chef

review_images_api_blueprint = Blueprint('review_images_api', __name__)



# POST /review_images/new - Post list of review images
@review_images_api_blueprint.route('/new', methods=["POST"])
def new_review_image():
    # if request.files["image_url"]:
    #     file= request.files.get("image_url")
    #     s3.upload_fileobj(
    #         file,
    #         os.getenv("S3_BUCKET"),
    #         file.filename,
    #         ExtraArgs={
    #             "ACL": "public-read",
    #             "ContentType": file.content_type
    #         }
    #     )
    #     image_url = f"https://{os.getenv('S3_BUCKET')}.s3-ap-southeast-1.amazonaws.com/{file.filename}"
    review_id = request.json.get("review_id", None)
    existing_review = Review.get_or_none(Review.id == review_id)
    user_id = request.json.get("user_id", None)
    existing_user = User.get_or_none(User.id == user_id)
    image_url = request.json.get("image_url", None)
    if existing_review == None:
        return jsonify(message="Review does not exist", status="Failed"), 400
    if existing_user == None:
        return jsonify(message="User does not exist", status="Failed"), 400
    if existing_review and existing_user:
        new_review_image = ReviewImage(review=review_id, user=user_id, image_url=image_url)
        if new_review_image.save():
            return jsonify({
                "message": "successfully posted review image",
                "status": "success",
                "review_id": review_id,
                "image_url": image_url,
                "user_id": user_id 
            })
        else:
            return jsonify({
                "message": "failed to post",
                "status": "failed"
            }), 400

# GET /review_images/<chef_id> - Return list of likes for a chef
@review_images_api_blueprint.route('/<chef_id>', methods=["GET"])
def review_images(chef_id):
    existing_chef = Chef.get_or_none(Chef.id == chef_id)
    if existing_chef == None:
        return jsonify(message="This chef does not exist", status="Failed"), 400
    existing_reviews = Review.get_or_none(Review.chef_id == chef_id)
    if existing_reviews:
        review_images = ReviewImage.select().join(Review).where(Review.chef_id == chef_id)
        if review_images:
            results = [{
                "review_image_id" : images.id,
                "user_id" : images.user_id,
                "review_id" : images.review_id,
                "image_url" : images.image_url,
            } for images in review_images]
            return jsonify(results), 200
        else: 
            return jsonify(message="This chef has no review images for any of his reviews", status="Failed"), 400
    else: 
        return jsonify(message="This chef does not have reviews yet, hence no images can be retrieved", status="Failed"), 400


# DELETE /review_images/delete/<chef_id> 
@review_images_api_blueprint.route('/delete/<review_images_id>', methods=["DELETE"])
def delete(review_images_id):
    existing_review_image = ReviewImage.get_or_none(ReviewImage.id == review_images_id)
    if existing_review_image:
        if existing_review_image.delete_instance():
            return jsonify(message="Successfully deleted this review image", status="Success"), 200
    else:
        return jsonify(message="This review image does not exist", status="Failed"), 400 

    