#!/usr/bin/python3
"""
User SignUp, SignIn
"""

from flask import Flask, render_template, request, url_for, redirect, make_response, jsonify
from flask import abort
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
from models.user import User
from models.service import Service
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
            return make_response(redirect(url_for('sign_in')))
        try:
            data = decode_token(token, app.secret_key)
            user_id = data["user_id"]
        except jwt.ExpiredSignatureError:
            return make_response(redirect(url_for('sign_in')))
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
    else:
        user = None

    return render_template("home.html", title="Home", user=user)

@app.route("/signup", strict_slashes=False, methods=["GET"])
def sign_up():
    if request.cookies.get("jwt_token"):
        abort(404)
    form = RegistrationForm()
    cities = []
    for key, value in storage.all(City).items():
        cities.append(value)

    return render_template("signup.html", title="SignUp", form=form, cities=cities)


@app.route("/signin", strict_slashes=False, methods=["GET"])
def sign_in():
    if request.cookies.get("jwt_token"):
        abort(404)
    form = LoginForm()
    return render_template("signin.html", title="SignIn", form=form)


@app.route("/signup", strict_slashes=False, methods=["POST"])
def sign_up_register():
    form = RegistrationForm()
    if form.validate_on_submit():
        data = {}
        for key, value in request.form.items():
            x = ["csrf_token", "submit"]
            if key not in x:
                data[key] = value

        print(data)

        head = {"x-api-key": API_KEY}

        res = requests.post(f"{API_URL}/api/v1/user", json=data, headers=head)
        
        if res.status_code == 201:
            return redirect(url_for('home_page'))

        else:
            return res.json()
    else:
        return redirect(url_for('sign_up'))


@app.route("/signin", strict_slashes=False, methods=["POST"])
def signin_action():
    form = LoginForm()
    if form.validate_on_submit():
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
            response = make_response(redirect(url_for('home_page')), 302)
            if expire_date:
                response.set_cookie('jwt_token', token, httponly=True,
                                max_age=30*24*60*60)
            else:
                response.set_cookie('jwt_token', token, httponly=True)

            return response

        else:
            return res.json()
    else:
        return render_template("signin.html", title="Sign In", form=form)


@app.route("/logout", strict_slashes=False, methods=["GET"])
@token_required
def logout(user_id):
    response = make_response(redirect(url_for('home_page')))
    response.set_cookie('jwt_token','', httponly=True, expires=0)
    return response


@app.route("/clinic", strict_slashes=False, methods=["GET"])
@token_required
def clinic_register(user_id):
    print(user_id)
    services = []
    for key, value in storage.all(Service).items():
        services.append(value)

    cities = []
    for key, value in storage.all(City).items():
        cities.append(value)

    form = ClinicForm()
    return render_template("clinic_reg.html", title="Clinic Registration", form=form,
                            services=services, cities=cities)


@app.route("/clinic", strict_slashes=False, methods=["POST"])
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

        head = {"x-api-key": API_KEY}

        res = requests.post(f"{API_URL}/api/v1/user/clinic", json=data, headers=head)
        if res.status_code == 201:
            print("CREATED")
            return make_response(redirect(url_for('home_page')))
        else:
            return res.json()
    else:
        return make_response(redirect(url_for('clinic_register')))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
