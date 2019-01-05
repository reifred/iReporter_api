from flask import Flask, jsonify, request
from app.models import Incident, User
from datetime import datetime

from app.validators import(
    validate_input, validate_comment, validate_location,
    validate_user_input, validate_status)

from app.helpers import(
    encode_token, decoded_token, extract_token_from_header,
    token_required, get_current_identity,
    non_admin, admin_required
)

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

red_flags, users = [], []


@app.route("/")
def index():
    return "Welcome to api."


@app.route("/api/v1/auth/sign_up", methods=["POST"])
def sign_up():
    """
    This function adds a user with unique (username and email)
    in the list of users and an admin cannot register
    """
    response = None
    data = request.get_json()
    if not request.is_json:
        return jsonify({
            "status": 400,
            "error": "JSON request required"
        }), 400
    firstname = data.get("firstname")
    lastname = data.get("lastname")
    othernames = data.get("othernames")
    email = data.get("email")
    phoneNumber = data.get("phoneNumber")
    username = data.get("username")
    password = data.get("password")
    registered = datetime.now().strftime("%Y-%m-%d")
    isAdmin = 0

    errors = validate_user_input(
        firstname, lastname, email, phoneNumber,
        username, password)

    if errors:
        return jsonify({"status": 400, "error": errors}), 400

    user = [user for user in users if user["username"] == username
            or user["email"] == email and user["isAdmin"] == isAdmin]

    if user:
        response = jsonify({
            "status": 400,
            "error": "username or email already exists"
        }), 400
    else:
        password_hash = generate_password_hash(password, method="sha256")
        guest = User(
            firstname, lastname, othernames, email, phoneNumber,
            username, password_hash, registered, isAdmin)
        users.append(guest.convert_to_dict())

        response = jsonify({
            "status": 201,
            "data": [{
                "id": guest._id,
                "username": guest.username,
                "message": "User registered"
            }]
        }), 201
    return response


@app.route("/api/v1/auth/sign_in", methods=["POST"])
def sign_in():
    """
    This function enables a registered user or admin to login
    """
    response = None
    user = request.get_json()
    if not request.is_json:
        return jsonify({
            "status": 400,
            "error": "JSON request required"
        }), 400

    username = user.get("username")
    password = user.get("password")
    isAdmin = user.get("isAdmin")

    if username == "admin" and password == "admin@33" and isAdmin == 1:
        token = encode_token(id(1),isAdmin)
        response = jsonify({
            "status": 201,
            "data": [{
                "token": token,
                "message": "Admin login",
                "username": "admin"
            }]
        }), 201
    else:
        user = [user for user in users if user["username"] == username
                and check_password_hash(user["password"], password)
                and user["isAdmin"] == isAdmin]
        if not user:
            response = jsonify({
                "status": 400,
                "error": "User doesnt exist"
            }), 400
        else:
            user_id = user[0]["_id"]
            token = encode_token(user_id, isAdmin)
            response = jsonify({
                "status": 201,
                "data": [{
                    "id": user_id,
                    "message": "User login",
                    "username": username,
                    "token": token
                }]
            }), 201
    return response
