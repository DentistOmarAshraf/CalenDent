#!/usr/bin/python3
"""
Clinic API
"""

from .__init__ import app_views, API_KEY, check_api_key
from models import storage
from models.user import User, RoleType
from models.clinic import Clinic
from models.address import Address
from models.neighborhood import Neighborhood
from models.service import Service
from flask import make_response, abort, request
from sqlalchemy.exc import IntegrityError
from datetime import time
from json import dumps


@app_views.route("/user/clinic", strict_slashes=False, methods=["POST"])
@check_api_key
def add_clinic():
    """Adding Clinic That belond to User"""
    try:
        data = request.get_json()
    except Exception:
        return make_response("Not A JSON", 401)

    the_user = storage.get(User, data["user_id"])
    if not the_user:
        abort(404)

    the_neighborhood = storage.get(Neighborhood, data["neighborhood_id"])
    if not the_neighborhood:
        abort(404)
    try:
        new_clinic = Clinic(
                name = data["name"],
                visit_price = data["visit_price"],
                opening_time = time(int(data["time_from"].split(':')[0]),
                                    int(data["time_from"].split(':')[1])),
                closing_time = time(int(data["time_to"].split(':')[0]),
                                    int(data["time_to"].split(':')[1]))
                )

        new_address = Address(text_address=data["address"])
        the_neighborhood.addresses.append(new_address)

        the_neighborhood.clinics.append(new_clinic)
        new_address.clinics.append(new_clinic)
        the_user.clinics.append(new_clinic)

        for service_id in data["services"]:
            new_clinic.services.append(storage.get(Service, service_id))
        
        storage.new(new_clinic)
        storage.new(new_address)
        storage.new(the_user)
        storage.new(the_neighborhood)
        the_user.role = RoleType.DOCTOR
        storage.save()
    except IntegrityError as e:
        dt = {"error": "Clinic exists"}
        res = make_response(dumps(dt, indent=4), 401)
        res.headers["Content-type"] = "application/json"
        return res

    to_ret = new_clinic.to_dict()
    if "address" in to_ret.keys():
        del (to_ret["address"])
    if "services" in to_ret.keys():
        del (to_ret["services"])
    if "user" in to_ret.keys():
        del (to_ret["user"])
    if "opening_time" in to_ret.keys():
        del (to_ret["opening_time"])
    if "closing_time" in to_ret.keys():
        del (to_ret["closing_time"])
    if "neighborhood" in to_ret.keys():
        del (to_ret["neighborhood"])
    res = make_response(dumps(to_ret, indent=4), 201)
    res.headers["Content-type"] = "application/json"
    return res

@app_views.route("/neighborhood/<neighborhood_id>/clinics",
                 strict_slashes=False, methods=["GET"])
def get_clinics_in_neighborhood(neighborhood_id):
    """GET all clinics in one neighborhood"""
    the_neighborhood = storage.get(Neighborhood, neighborhood_id)
    if not the_neighborhood:
        abort(404)

    to_ret = []
    for clinic in the_neighborhood.clinics:
        cl_dict = clinic.to_dict()
        if "address" in cl_dict.keys():
            del (cl_dict["address"])
        if "services" in cl_dict.keys():
            del (cl_dict["services"])
        if "user" in cl_dict.keys():
            del (cl_dict["user"])
        if "opening_time" in cl_dict.keys():
            del (cl_dict["opening_time"])
        if "closing_time" in cl_dict.keys():
            del (cl_dict["closing_time"])
        if "neighborhood" in cl_dict.keys():
            del (cl_dict["neighborhood"])
        to_ret.append(cl_dict)
    
    print(to_ret)
    res = make_response(dumps(to_ret, indent=4), 200)
    res.headers["Content-type"] = "application/json"
    return res
