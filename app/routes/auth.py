from flask import Blueprint, jsonify, request
from app.models.models import User
from datetime import datetime

from app.helpers.validators import validate_user_input, validate_sign_in

from app.helpers.helpers import encode_token, token_required, admin_required

from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/v1")

users = []
response = None


@auth_bp.route("/auth/sign_up", methods=["POST"])
def sign_up():
    """
    This function adds a user with unique (username and email)
    in the list of users
    """
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

    user = [user for user in users if user["username"] == username
            or user["email"] == email and user["isAdmin"] == isAdmin]

    errors = validate_user_input(
        firstname, lastname, email, phoneNumber,
        username, password)

    if errors:
        response = jsonify({"status": 400, "error": errors}), 400
    elif user:
        response = jsonify({"status": 400,
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


@auth_bp.route("/auth/sign_in", methods=["POST"])
def sign_in():
    """
    This function checks whether the user exists
    before login
    """
    if not request.is_json:
        return jsonify({
            "status": 400,
            "error": "JSON request required"
        }), 400

    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    isAdmin = data.get("isAdmin")

    user_verified = User.verify_user(data, users, username, password, isAdmin)

    errors = validate_sign_in(username, password)

    if username == "admin" and password == "admin@33" and isAdmin == 1:
        token = encode_token(id(1), isAdmin)
        response = jsonify({
            "status": 201,
            "data": [{
                "token": token,
                "message": "Admin login",
                "username": "admin"
            }]
        }), 201
    elif errors:
        response = jsonify({"status": 400, "error": errors}), 400
    elif not User.username_exists(username,users):
        response = jsonify({
            "status": 400,
            "error": "Username doesnt exist"
        }), 400
    elif not user_verified:
        response = jsonify({
            "status": 400,
            "error": "Enter correct password"
        }), 400
    else:
        user_id = user_verified[0]["_id"]
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


@auth_bp.route("/users", methods=["GET"])
@token_required
@admin_required
def get_all_registered_users():
    """Get all registered users"""
    return jsonify({
        "status": 200,
        "data": [{
            "Number of users": len(users),
            "users": users
        }]
    })
