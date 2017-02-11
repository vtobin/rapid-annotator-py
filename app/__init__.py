from flask import Flask

annotator = Flask(__name__)
from app import views

