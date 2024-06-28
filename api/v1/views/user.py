#!/usr/bin/python3
"""
User API
"""

from .__init__ import app_views
from flask import make_response, request
from models import storage
from models.user import User
from json import dumps
from sqlalchemy.exc import IntegrityError

@app_views.route("/user", strict_slashes=False, methods=["POST"])
def new_user():
    try:
        data = request.get_json()
    except Exception:
        return make_response("Not A JSON", 400)

    if "email" not in data.keys() or not len(data["email"]):
        return make_response("email missing", 400)

    if "password" not in data.keys() or not len(data["password"]):
        return make_response("password missing", 400)

    try:
        new_user = User(**(data))
        storage.new(new_user)
        storage.save()
    except IntegrityError as e:
        print(e)
        dt = {"error": "email present"}
        res = make_response(dumps(dt), 400)
        res.headers["Content-type"] = "application/json"
        return res

    res = make_response(dumps(new_user.to_dict(), indent=4), 201)
    res.headers["Content-type"] = "application/json"
    return res
