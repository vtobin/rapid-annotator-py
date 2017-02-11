from flask import Flask

annotator = Flask(__name__, static_url_path='/static')
from app import views, utils, db

@annotator.before_request
def before_request():
    db.db.connect()

@annotator.after_request
def after_request(response):
    db.db.close()
    return response
