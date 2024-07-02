#!/usr/bin/python3
"""
User API
"""

from .__init__ import app_views, API_KEY, check_api_key
from flask import make_response, request, abort
from models import storage
from models.user import User
from models.neighborhood import Neighborhood
from models.address import Address
from json import dumps
from sqlalchemy.exc import IntegrityError
from functools import wraps
from os import getenv


@app_views.route("/check_user", strict_slashes=False, methods=["POST"])
def check_user():
    """Check User and password in Database"""
    try:
        data = request.get_json()
    except Exception:
        return make_response("Not A JSON", 400)

    if "email" not in data.keys():
        return make_response("Missing email", 400)

    if "password" not in data.keys():
        return make_response("Missing password", 400)

    the_user = storage.get_by(User, "email", data["email"])
    if the_user is None:
        res = make_response(dumps({"error": "user not found"}), 404)
        res.headers["Content-type"] = "application/json"
        return res

    chk_pass = the_user.verify_password(data["password"])
    if not chk_pass:
        res = make_response(dumps({"error": "Incorrect password"}), 401)
        res.headers["Content-type"] = "application/json"
        return res
    else:
        user_dict = the_user.to_dict()
        if "role" in user_dict.keys():
            del (user_dict["role"])
        res = make_response(dumps(user_dict), 200)
        res.headers["Content-type"] = "application/json"
        return res


@app_views.route("/user", strict_slashes=False, methods=["POST"])
@check_api_key
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
        new_user = User(
                email = data["email"],
                password = data["password"],
                username = data["username"],
                first_name = data["first_name"],
                last_name = data["last_name"],
                role = "user"
                )
        new_address = Address(text_address = data["address"])
        new_address.users.append(new_user)
        new_address.neighborhood = storage.get(Neighborhood, data["neighborhood"])
        storage.new(new_user)
        storage.new(new_address)
        storage.save()
    except IntegrityError as e:
        print(e)
        dt = {"error": "email present"}
        res = make_response(dumps(dt, indent=4), 400)
        res.headers["Content-type"] = "application/json"
        return res
    
    to_ret = new_user.to_dict()
    if "address" in to_ret.keys():
        del (to_ret["address"])
    res = make_response(dumps(to_ret, indent=4), 201)
    res.headers["Content-type"] = "application/json"
    return res
