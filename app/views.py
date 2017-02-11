from flask import render_template
from app import annotator

@annotator.route("/")
@annotator.route("/index")
def index():
    user = {"nickname": "Friend"}
    return render_template("index.html", user=user)

@annotator.route("/friend/<name>")
def friend(name):
    user = {"nickname": name}
    return render_template("index.html", user=user)

