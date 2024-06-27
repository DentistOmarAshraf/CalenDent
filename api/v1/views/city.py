#!/usr/bin/python3
"""
City Model
"""

from models import storage
from flask import make_response, request, abort
from json import dumps
from .__init__ import app_views
from models.city import City
from sqlalchemy.exc import IntegrityError


@app_views.route("/city", strict_slashes=False, methods=["GET"])
def all_cities():
    """Return all Cities in Data Base"""

    to_ret = []
    for key, value in storage.all(City).items():
        to_ret.append(value.to_dict())

    res = make_response(dumps(to_ret, indent=4), 200)
    res.headers["Content-type"] = "application/json"
    return res

@app_views.route("/city", strict_slashes=False, methods=["POST"])
def add_city():
    try:
        data = request.get_json()
    except Exception:
        return make_response("Not a JSON", 400)

    if "name" not in data.keys():
        return make_response("City Name Missing", 400)

    try:
        new_city = City(**(data))
        storage.new(new_city)
        storage.save()
    except IntegrityError:
        return make_response("Unable to Save City", 400)

    res = make_response(dumps(new_city.to_dict(), indent=4), 200)
    res.headers["Content-type"] = "application/json"
    return res


@app_views.route("/city/<city_id>", strict_slashes=False, methods=["GET"])
def one_city(city_id):
    """Return Info of one City"""
    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)
    
    res = make_response(dumps(the_city.to_dict(), indent=4), 200)
    res.headers["Content-type"] = "application/json"
    return res

@app_views.route("/city/<city_id>", strict_slashes=False, methods=["DELETE"])
def del_city(city_id):
    """Delete city from DataBase"""
    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)
    the_city.delete()
    res = make_response(dumps({}), 200)
    res.headers["Content-type"] = "application/json"
    return res

@app_views.route("/city/<city_id>", strict_slashes=False, methods=["PUT"])
def modify_city(city_id):
    """change data of city"""
    try:
        data = request.get_json()
    except Exception:
        return make_response("Not a JSON", 400)

    if "name" not in data.keys():
        return make_response("Missing Name", 401)

    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)

    for key, value in data.items():
        restriction = ["id", "updated_at", "created_at"]
        if key not in restriction:
            setattr(the_city, key, value)

    storage.save()

    res = make_response(dumps(the_city.to_dict(), indent=4), 200)
    res.headers["Content-type"] = "application/json"
    return res
