from flask import abort, jsonify, render_template, redirect, request, url_for
from app import annotator, utils, models
from app.models import User, DataType, TagSet, Tag, TagRun
from playhouse.shortcuts import model_to_dict

@annotator.route("/")
@annotator.route("/index")
def index():
    return render_template("index.html")

@annotator.route("/tagrun/<name>")
def tagrun(name):
    # TODO: This should be handled by a cookied session and
    # redirect to the login screen rather than the index
    user = request.args.get("user")
    if not user:
        return redirect(url_for("index"))
    try:
        tagset = models.TagSet.get(TagSet.name == name)
    except TagSet.DoesNotExist:
        return redirect(url_for("index"))
    data_type = tagset.data_type
    # TODO This should be dispatched.
    images = utils.images_from_local_directory(tagset.data_info)
    tags = {}
    button_count = 1
    for t in Tag.select().where(Tag.tagset_id == tagset.id):
        tags[button_count] = t.name
        button_count += 1
    model_obj = model_to_dict(tagset)
    model_obj['initialImage'] = url_for('static', filename=images[0])
    model_obj['tags'] = tags
    return render_template("tagrun.html", tagrun=model_obj)

@annotator.route("/tagrun/<name>/response", methods=["POST"])
def tagrun_response(name):
    # TODO: This should be handled by a cookied session
    username = request.args.get("user")
    if not username:
        return abort(400)
    # TODO: This should be moved into a separate setup step elsewhere.
    try:
        user = User.get(User.username == username)
    except User.DoesNotExist:
        new_user = User(username=username, email=username + '@example.com')
        new_user.save()
        user = new_user
    val = request.json
    try:
        tagset = models.TagSet.get(TagSet.name == name)
    except TagSet.DoesNotExist:
        return abort(400)
    if val.get('imageIndex', None) is None or not\
            isinstance(val['imageIndex'], int):
        # TODO; Log 
        print(val['imageIndex'])
        print(type(val['imageIndex']))
        return abort(400)
    # TODO also needs dispatch
    images = utils.images_from_local_directory(tagset.data_info)
    if val['imageIndex'] >= len(images):
        # TODO; Log 
        return abort(400)
    # TODO: VALIDATE RESPONSE HERE ("tagged")
    response = TagRun(tagset=name, user=user, data_item=val['imageIndex'], response=val['tagged'])
    response.save()
    r = {"success": True}
    if val['imageIndex'] + 1 == len(images):
        r['finished'] = True
    else:
        r['finished'] = False
        r['nextImage'] = url_for('static',
            filename=images[val['imageIndex'] + 1])
    return jsonify(r)
