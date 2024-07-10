#!/usr/bin/python3
"""
Reservation API
"""

from .__init__ import app_views
from models import storage
from models.reservation import Reservation, Status
from flask import make_response, abort, request
from json import dumps


@app_views.route("/reservation/<reservation_id>", strict_slashes=False, methods=["GET"])
def reservation_action(reservation_id):
    """Get Info about reservation and Change status of reservation"""
    the_reservation = storage.get(Reservation, reservation_id)
    if not the_reservation:
        abort(404)

    action = request.args.get('action')
    if not action:
        abort(404)

    actions = ["confirmed", "declined", "delete"]
    if action not in actions:
        abort(404)

    if action == "confirmed":
        the_reservation.status = Status.CONFIRMED
    if action == "declined":
        the_reservation.status = Status.DECLINED
    if action == "delete":
        the_reservation.delete()

    storage.save()
    
    to_ret = {}
    to_ret["id"] = the_reservation.id
    to_ret["user"] = the_reservation.user.email
    to_ret["phone"] = the_reservation.phone
    to_ret["status"] = the_reservation.status.value
    res = make_response(dumps(to_ret, indent=4), 200)
    res.headers["Content-type"] = "application/json"
    return res
