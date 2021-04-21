import os
import config
import boto3, botocore
from flask import Flask
from models.base_model import db

web_dir = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), 'foodapp_web')

app = Flask('FOODAPP', root_path=web_dir)

if os.getenv('FLASK_ENV') == 'production':
    app.config.from_object("config.ProductionConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

s3 = boto3.client(
    "s3",
    aws_secret_access_key= "XXX",
    aws_access_key_id= "XXX",
)

@app.before_request
def before_request():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        print(db)
        print(db.close())
    return exc