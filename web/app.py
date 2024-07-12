#!/usr/bin/python3
"""
User SignUp, SignIn
"""

from flask import Flask, render_template, request
from flask import url_for, redirect, make_response, jsonify
from flask import abort, flash
from flask_cors import CORS
import requests
from .registration_form import RegistrationForm
from .login_form import LoginForm
from .clinic_form import ClinicForm
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from models import storage
from models.city import City
from models.user import User, RoleType
from models.service import Service
from models.clinic import Clinic
from json import dumps
from functools import wraps
from .helper_function import create_token, decode_token
from datetime import datetime
from datetime import timedelta
import jwt


app = Flask(__name__)
app.secret_key = "985e88a9260210904300cd5d50558197"
CORS(app, supports_credentials=True)
JWT = JWTManager(app)
API_KEY = "API_SECRET_KEY"
API_URL = "http://localhost:5001"


def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.cookies.get('jwt_token')
        if not token:
            next_url = request.url
            return make_response(redirect(url_for('sign_in', next=next_url)))
        try:
            data = decode_token(token, app.secret_key)
            user_id = data["user_id"]
        except jwt.ExpiredSignatureError:
            res = make_response(redirect(url_for('sign_in')))
            res.set_cookie('jwt_token', '', httponly=True, expires=0)
            return res
        except jwt.InvalidTokenError:
            return make_response(redirect(url_for('sign_in')))

        return func(user_id, *args, **kwargs)

    return decorated


@app.route("/", strict_slashes=False, methods=["GET"])
def home_page():
    token = request.cookies.get('jwt_token')
    if token:
        data = decode_token(token, app.secret_key)
        user = storage.get(User, data["user_id"])
        clinics = user.address.neighborhood.clinics
    else:
        user = None
        clinics = storage.all(Clinic).values()

    cities = storage.all(City).values()

    return render_template("home.html",
                           title="Home",
                           user=user,
                           cities=cities,
                           clinics=clinics)


@app.route("/signup", strict_slashes=False, methods=["GET"])
def sign_up():
    if request.cookies.get("jwt_token"):
        abort(404)
    form = RegistrationForm()
    cities = []
    for key, value in storage.all(City).items():
        cities.append(value)

    return render_template("signup.html",
                           title="SignUp",
                           form=form,
                           cities=cities)


@app.route("/signin", strict_slashes=False, methods=["GET"])
def sign_in():
    if request.cookies.get("jwt_token"):
        abort(404)
    form = LoginForm()
    next_url = request.args.get('next')
    return render_template("signin.html",
                           title="SignIn",
                           form=form,
                           url=next_url)


@app.route("/signup", strict_slashes=False, methods=["POST"])
def sign_up_register():
    form = RegistrationForm()
    if form.validate_on_submit():
        data = {}
        for key, value in request.form.items():
            x = ["csrf_token", "submit"]
            if key not in x:
                data[key] = value

        head = {"x-api-key": API_KEY}

        res = requests.post(f"{API_URL}/api/v1/user", json=data, headers=head)
        
        if res.status_code == 201:
            flash(f'Successfully Created for {res.json()["username"]}', 'success')
            return redirect(url_for('home_page'))

        else:
            flash(res.json()["err"], 'error')
            return redirect(url_for('sign_up'))
    else:
        return redirect(url_for('sign_up'))


@app.route("/signin", strict_slashes=False, methods=["POST"])
def signin_action():
    form = LoginForm()
    if form.validate_on_submit():
        next_url = request.form.get('next_url')
        data = {}
        data["email"] = request.form["email"]
        data["password"] = request.form["password"]

        if "remember" in request.form.keys():
            expire_date = timedelta(days=30)
        else:
            expire_date = None

        res = requests.post(f"{API_URL}/api/v1/check_user", json=data)
        if res.status_code == 200:
            user_data = res.json()
            token = create_token(user_data, app.secret_key, expire_date)
            response = make_response(
                                redirect(next_url or url_for('home_page')),
                                302)
            if expire_date:
                response.set_cookie('jwt_token', token, httponly=True,
                                    max_age=30*24*60*60)
            else:
                response.set_cookie('jwt_token', token, httponly=True)

            flash(f'Signed In as {user_data["username"]}', 'success')
            return response

        else:
            flash(f'{res.json()["err"]}', 'error')
            return redirect(url_for('sign_in'))
    else:
        flash(f'Email or password Field Error', 'error')
        return render_template("signin.html", title="Sign In", form=form)


@app.route("/logout", strict_slashes=False, methods=["GET"])
@token_required
def logout(user_id):
    response = make_response(redirect(url_for('home_page')))
    response.set_cookie('jwt_token', '', httponly=True, expires=0)
    return response


@app.route("/clinic_reg", strict_slashes=False, methods=["GET"])
@token_required
def clinic_register(user_id):
    the_user = storage.get(User, user_id)
    services = []
    for key, value in storage.all(Service).items():
        services.append(value)

    cities = []
    for key, value in storage.all(City).items():
        cities.append(value)

    form = ClinicForm()
    return render_template("clinic_reg.html",
                           title="Clinic Registration",
                           form=form,
                           services=services,
                           cities=cities,
                           user=the_user)


@app.route("/clinic_reg", strict_slashes=False, methods=["POST"])
@token_required
def clinic_register_action(user_id):
    form = ClinicForm()
    if form.validate_on_submit():
        services = []
        for k, v in request.form.items():
            if k.split('.')[0] == "service":
                services.append(v)

        data = {}
        data["user_id"] = user_id
        data["name"] = request.form.get("name")
        data["address"] = request.form.get("address")
        data["neighborhood_id"] = request.form.get("neighborhood")
        data["time_from"] = request.form.get("time_from")
        data["time_to"] = request.form.get("time_to")
        data["visit_price"] = request.form.get("visit_price")
        data["services"] = services
        data["duration"] = request.form.get("duration")

        head = {"x-api-key": API_KEY}

        res = requests.post(f"{API_URL}/api/v1/user/clinic",
                            json=data, headers=head)
        if res.status_code == 201:
            flash(f'Succesfully Created Clinic {res.json()["name"]}', 'success')
            return make_response(redirect(url_for('home_page')))
        else:
            flash(f'{res.json()["err"]}', 'error')
            return res.json()
    else:
        flash(f'Error !', 'error')
        return make_response(redirect(url_for('clinic_register')))


@app.route("/book", strict_slashes=False, methods=["GET"])
@token_required
def make_reservation(user_id):
    the_user = storage.get(User, user_id)
    if the_user.role != RoleType.USER:
        res = make_response(dumps({"err": "Unauthorized"}), 401)
        res.headers["Content-type"] = "application/json"
        return res
    clinic_id = request.args.get('clinic_id')
    if not clinic_id:
        return make_response(redirect(url_for('home_page')))
    the_clinic = storage.get(Clinic, clinic_id)
    for reservation in the_clinic.reservations:
        if reservation.user == the_user:
            flash('You already Booked! Check Your Reservations', 'error')
            return redirect(url_for('home_page'))
    return render_template("reservation.html",
                           title=f"Reservation {the_clinic.name}",
                           clinic=the_clinic,
                           user=the_user)


@app.route("/book", strict_slashes=False, methods=["POST"])
@token_required
def make_reservation_action(user_id):
    clinic_id = request.form.get("clinic_id")
    phone = request.form.get("phone")
    appointment = request.form.get("appointment")

    if not clinic_id:
        return make_response(redirect_for(url_for('make_reservation')))
    if not phone:
        flash('Fill out Phone Number', 'error')
        return make_response(redirect_for(url_for('make_reservation')))
    if not appointment:
        flash('Fill out Time of Your reservation', 'error')
        return make_response(redirect_for(url_for('make_reservation')))

    the_user = storage.get(User, user_id)

    the_clinic = storage.get(Clinic, clinic_id)
    for reservation in the_clinic.reservations:
        if reservation.user == the_user:
            res = make_response(dumps({"err": "you have already one"}), 401)
            res.headers["Content-type"] = "application/json"
            return res

    data = {}
    data["user_id"] = user_id
    data["phone"] = phone
    data["appointment"] = appointment

    head = {"x-api-key": API_KEY}

    res = requests.post(f"{API_URL}/api/v1/clinic/{clinic_id}/reservation",
                        json=data,
                        headers=head)
    if res.status_code == 201:
        flash(f'Successfully Booked reservation at {res.json()["clinic"]}', 'success')
        return make_response(redirect(url_for('home_page')))
    else:
        flash(f'{res.json()["err"]} Check Out Your Reservations', 'error')
        return redirect(url_for('home_page'))


@app.route("/clinic_control", strict_slashes=False, methods=["GET"])
@token_required
def clinic_control(user_id):
    """Control over clinics and reservations"""
    the_user = storage.get(User, user_id)
    if the_user.role != RoleType.DOCTOR:
        res = make_response(dumps({"err": "Unauthorized"}), 401)
        res.headers["Content-type"] = "application/json"
        return res

    return render_template("clinic_control.html",
                           clinics=the_user.clinics,
                           user=the_user,
                           title=f"Controller {the_user.first_name}")


@app.route("/user_reservations", strict_slashes=False, methods=["GET"])
@token_required
def user_reservation_control(user_id):
    """User Reservation page to Know status of the visit or Cancel it"""
    the_user = storage.get(User, user_id)
    if the_user.role != RoleType.USER:
        flash('Unauthorized Access !', 'error')
        return redirect(url_for('home_page'))

    return render_template("user_control.html",
                           reservations=the_user.reservations,
                           user=the_user,
                           title=f"Your Reservations")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
