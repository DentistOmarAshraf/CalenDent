#!/usr/bin/python3
"""
Clinic API
"""

from .__init__ import app_views, API_KEY, check_api_key
from models import storage
from models.user import User, RoleType
from models.clinic import Clinic
from models.address import Address
from models.reservation import Reservation, Status
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
                                    int(data["time_to"].split(':')[1])),
                visit_duration = time(int(data["duration"].split(':')[0]),
                                      int(data["duration"].split(':')[1]))
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
        dt = {"err": "Clinic exists"}
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
    if "visit_duration" in to_ret.keys():
        del (to_ret["visit_duration"])
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

    owner = request.args.get('owner')
    to_ret = []
    if owner:
        clinics = storage.search_related(Clinic,"username", User, owner)
        for clinic in clinics:
            load = [clinic.user, clinic.address, clinic.reviews]
            if clinic.neighborhood != the_neighborhood:
                continue
            else:
                to_ret.append(clinic.to_dict())
    else:
        for clinic in the_neighborhood.clinics:
            load = [clinic.user, clinic.address, clinic.neighborhood, clinic.reviews]
            to_ret.append(clinic.to_dict())

    for cl_dict in to_ret:
        if "opening_time" in cl_dict.keys():
            cl_dict["opening_time"] = cl_dict["opening_time"].strftime('%H:%M')
        if "closing_time" in cl_dict.keys():
            cl_dict["closing_time"] = cl_dict["closing_time"].strftime('%H:%M')
        if "visit_duration" in cl_dict.keys():
            del (cl_dict["visit_duration"])
        if "address" in cl_dict.keys():
            cl_dict["address"] = cl_dict["address"].text_address
        if "user" in cl_dict.keys():
            cl_dict["user"] = f'{cl_dict["user"].first_name} {cl_dict["user"].last_name}'
        if "neighborhood" in cl_dict.keys():
            cl_dict["neighborhood"] = cl_dict["neighborhood"].name
        if "reviews" in cl_dict.keys():
            num = 0
            total = 0
            for review in cl_dict["reviews"]:
                num += 1
                total += review.stars
            if num != 0:
                avg = total // num
            else:
                avg = "N/A"
            cl_dict["stars"] = avg
            del (cl_dict["reviews"])
    
    res = make_response(dumps(to_ret, indent=4), 200)
    res.headers["Content-type"] = "application/json"
    return res

@app_views.route("/clinic/<clinic_id>/reservation", strict_slashes=False, methods=["POST"])
@check_api_key
def make_new_reservation(clinic_id):
    try:
        data = request.get_json()
    except Exception:
        return make_response("Not A JSON", 401)

    the_clinic = storage.get(Clinic, clinic_id)
    if not the_clinic:
        res = make_response(dumps({"err": "Clinic Not Found"}), 404)
        res.headers["Content-type"] = "application/json"
        return res

    the_user = storage.get(User, data["user_id"])
    if not the_user:
        res = make_response(dumps({"err": "User not in data"}), 401)
        res.headers["Content-type"] = "application/json"
        return res

    if the_user.role == RoleType.DOCTOR:
        res = make_response(dumps({"err": "Unauthorized"}), 401)
        res.headers["Content-type"] = "application/json"
        return res

    for reservation in the_clinic.reservations:
        if reservation.user == the_user:
            res = make_response(dumps({"err": "You can't make reservation twice"}), 401)
            res.headers["Content-type"] = "application/json"
            return res

    try:
        new_reservation = Reservation(
                            phone=data["phone"],
                            status=Status.WAITING,
                            appointment=time(int(data["appointment"].split(':')[0]),
                                             int(data["appointment"].split(':')[1]))
                            )
        for reservation in the_user.reservations:
            if new_reservation.appointment == reservation.appointment:
                time_of_error = reservation.appointment.strftime("%H:%M")
                to_ret = {
                    "err": f'There Is Reservation At {time_of_error}'
                    }
                res = make_response(dumps(to_ret), 401)
                res.headers["Content-type"] = "application/json"
                return res
        the_clinic.reservations.append(new_reservation)
        the_user.reservations.append(new_reservation)
        storage.new(new_reservation)
        storage.new(the_clinic)
        storage.new(the_user)
        storage.save()

    except IntegrityError as e:
        print(e)
        dt = {"error": "Data error"}
        res = make_response(dumps(dt, indent=4), 401)
        res.headers["Content-type"] = "application/json"
        return res


    res_dict = new_reservation.to_dict()
    if "appointment" in res_dict.keys():
        res_dict["appointment"] = res_dict["appointment"].strftime("%H:%M")
    if "user" in res_dict.keys():
        res_dict["user"] = f'{res_dict["user"].first_name} {res_dict["user"].last_name}'
    if "clinic" in res_dict.keys():
        res_dict["clinic"] = res_dict["clinic"].name
    if "status" in res_dict.keys():
        res_dict["status"] = res_dict["status"].value

    res = make_response(dumps(res_dict), 201)
    res.headers["Content-type"] = "application/json"
    return res
