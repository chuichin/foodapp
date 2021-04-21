import os
from app import app, s3
from flask import Blueprint, Flask, jsonify, request
from models.review_image import ReviewImage

review_images_api_blueprint = Blueprint('review_images_api', __name__)

# GET /review_images/<chef_id> - Return list of likes for a chef
@review_images_api_blueprint.route('/<chef_id>', methods=["GET"])
def review_images(chef_id):
    review_images = ReviewImage.select().where(ReviewImage.chef == chef_id)
    ReviewImage = [{
        "id" : images.id,
        "user_id" : images.user,
        "review_id" : images.review,
        "image_url" : images.image_url
    } for images in review_images]
    return jsonify(ReviewImage)

# POST /review_images/new - Post list of review images
@review_images_api_blueprint.route('/new', methods=["POST"])
def new_review_image():
    if request.files["image_url"]:
        file= request.files.get("image_url")
        s3.upload_fileobj(
                    file,
                    os.getenv("S3_BUCKET"),
                    file.filename,
                    ExtraArgs={
                        "ACL": "public-read",
                        "ContentType": file.content_type
                    }
                )
        image_url = f"https://{os.getenv('S3_BUCKET')}.s3-ap-southeast-1.amazonaws.com/{file.filename}"
        review_id = request.json.get("review_id", None)
        user_id = request.json.get("user_id", None)
        new_review_image = ReviewImage(review=review_id, user=user_id, image_url=image_url)
        if new_review_image.save():
            return jsonify({
                "message": "successfully posted review image",
                "status": "success"
            })