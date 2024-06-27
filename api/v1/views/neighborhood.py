#!/usr/bin/python3
"""
Neighborhood API
"""

from .__init__ import app_views
from flask import make_response, abort, request
from json import dumps
from models.neighborhood import Neighborhood
from models.city import City
from models import storage


@app_views.route("/city/<city_id>/neighborhood", strict_slashes=False, methods=["GET"])       
def all_neighborhood(city_id):
    """Return all neighborhood in one city"""

    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)

    to_ret = []
    for neighborhood in the_city.neighborhoods:
        to_ret.append(neighborhood.to_dict())

    res = make_response(dumps(to_ret, indent=4), 200)
    res.headers["Content-type"] = "application/json"
    return res


@app_views.route("/city/<city_id>/neighborhood", strict_slashes=False, methods=["POST"])
def add_neighborhood(city_id):
    """Adding neighborhood to city"""
    try:
        data = request.get_json()
    except Exception:
        return make_response("Not A Json", 400)

    if "name" not in data.keys():
        return make_response("Missing Neighborhood name", 400)

    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)

    new_neighborhood = Neighborhood(**(data))
    the_city.neighborhoods.append(new_neighborhood)
    storage.new(new_neighborhood)
    storage.save()

    neighbor_dict = new_neighborhood.to_dict()
    if 'city' in neighbor_dict.keys():
        del (neighbor_dict["city"])

    res = make_response(dumps(neighbor_dict, indent=4), 201)
    res.headers["Content-type"] = "application/json"
    return res


@app_views.route("/city/<city_id>/neighborhood/<neighborhood_id>",
                 strict_slashes=False, methods=["GET"])
def one_neighborhood(city_id, neighborhood_id):
    """get info of one neighborhood"""
    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)
    
    the_neighborhood = storage.get(Neighborhood, neighborhood_id)
    if the_neighborhood is None:
        abort(404)


    if the_neighborhood not in the_city.neighborhoods:
        abort(404)

    res = make_response(dumps(the_neighborhood.to_dict(), indent=4), 200)
    res.headers["Content-type"] = "application/json"
    return res


@app_views.route("/city/<city_id>/neighborhood/<neighborhood_id>",
                 strict_slashes=False, methods=["DELETE"])
def delete_neighborhood(city_id, neighborhood_id):
    """DELETE neighborhood"""
    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)

    the_neighborhood = storage.get(Neighborhood, neighborhood_id)
    if the_neighborhood is None:
        abort(404)
    
    if the_neighborhood not in the_city.neighborhoods:
        abort(404)

    the_neighborhood.delete()

    res = make_response(dumps({}), 200)
    res.headers["Content-type"] = "application/json"
    return res


@app_views.route("/city/<city_id>/neighborhood/<neighborhood_id>",
                 strict_slashes=False, methods=["PUT"])
def modify_neighborhood(city_id, neighborhood_id):
    """Modify neighborhood"""
    try:
        data = request.get_json()
    except Exception:
        return make_response("Not A JSON", 400)

    the_city = storage.get(City, city_id)
    if the_city is None:
        abort(404)

    the_neighborhood = storage.get(Neighborhood, neighborhood_id)
    if the_neighborhood is None:
        abort(404)

    if the_neighborhood not in the_city.neighborhoods:
        abort(404)

    for key, value in data.items():
        restriction = ["id", "created_at", "updated_at"]
        if key not in restriction:
            setattr(the_neighborhood, key, value)

    storage.save()

    res = make_response(dumps(the_neighborhood.to_dict(), indent=4), 200)
    res.headers["Content-type"] = "application/json"
    return res
