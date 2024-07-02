#!/usr/bin/python3
"""
User SignUp, SignIn
"""

from flask import Flask, render_template, request, url_for, redirect, make_response, jsonify
from flask_cors import CORS
import requests
from .registration_form import RegistrationForm
from .login_form import LoginForm
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from models import storage
from models.city import City
from json import dumps
from functools import wraps
import jwt


app = Flask(__name__)
app.secret_key = "985e88a9260210904300cd5d50558197"
app.config["JWT_SECRET_KEY"] = "JWT_SECRET_KEY"
app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies", "json", "query_string"]
CORS(app, supports_credentials=True)
JWT = JWTManager(app)
API_KEY = "API_SECRET_KEY"
API_URL = "http://localhost:5001"


@app.route("/", strict_slashes=False, methods=["GET"])
def home_page():
    print(request.cookies.get('jwt_token'))
    return render_template("home.html", title="Home")

@app.route("/signup", strict_slashes=False, methods=["GET"])
def sign_up():
    form = RegistrationForm()
    cities = []
    for key, value in storage.all(City).items():
        cities.append(value)

    return render_template("signup.html", title="SignUp", form=form, cities=cities)


@app.route("/signin", strict_slashes=False, methods=["GET"])
def signin():
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
        
        res = requests.post(f"{API_URL}/api/v1/check_user", json=data)
        if res.status_code == 200:
            access = create_access_token(identity=data["email"])
            res = make_response(dumps({"Token": access}), 200)
            res.headers["Content-type"] = "application/json"
            res.set_cookie("jwt_token", access, httponly=True)
            return res

        else:
            return res.json()
    else:
        return render_template("signin.html", title="Sign In", form=form)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
