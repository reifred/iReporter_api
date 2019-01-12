from flask import Flask, jsonify, request
from app.models import Incident, User
from datetime import datetime

from app.validators import(
    validate_input, validate_edit_input,
    validate_user_input, validate_status,
    validate_sign_in)

from app.helpers import(
    encode_token, decoded_token, extract_token_from_header,
    token_required, get_current_identity,
    non_admin, admin_required
)

from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

red_flags, users = [], []
response = None


@app.route("/")
def index():
    return "Welcome to api."


@app.route("/api/v1/auth/sign_up", methods=["POST"])
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


@app.route("/api/v1/auth/sign_in", methods=["POST"])
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

    user = [data for data in users if data["username"] == username
            and check_password_hash(data["password"], password)
            and data["isAdmin"] == isAdmin]

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
    elif not user:
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


@app.route("/api/v1/red_flags", methods=["POST"])
@token_required
@non_admin
def create_red_flag_record_of_given_user():
    """Create a red flag of a given user"""
    if not request.is_json:
        response = jsonify({
            "status": 400,
            "error": "JSON request required"
        }), 400
    else:
        red_flag = request.get_json()
        createdOn = datetime.now().strftime("%Y-%m-%d")
        createdBy = get_current_identity()
        status = "draft"
        comment = red_flag.get("comment")
        _type = red_flag.get("_type")
        images = red_flag.get("images")
        videos = red_flag.get("videos")
        location = red_flag.get("location")

        errors = validate_input(location, comment, _type, images)

        if errors:
            response = jsonify({"status": 400, "error": errors}), 400
        else:
            incident = Incident(createdBy, createdOn, _type, location,
                                status, images, videos, comment)
            red_flags.append(incident.convert_to_dict())
            response = jsonify({
                "status": 201,
                "data": [{
                    "message": "Created red-flag record",
                    "id": incident._id
                }]
            }), 201
    return response


@app.route("/api/v1/auth/red_flags", methods=["GET"])
@token_required
@admin_required
def get_all_red_flag_records_admin():
    """Get all available red flags"""
    return jsonify({
        "data": red_flags,
        "status": 200
    }), 200


@app.route("/api/v1/users", methods=["GET"])
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


@app.route("/api/v1/red_flags/<int:red_flag_id>/status", methods=["PATCH"])
@token_required
@admin_required
def edit_status_of_user_red_flag(red_flag_id):
    """Edit the status of a user red flag"""
    red_flag = [
        red_flag for red_flag in red_flags if red_flag["_id"] == red_flag_id]
    if not red_flag:
        response = jsonify({
            "status": 400,
            "error": "ID Not found. Enter a valid ID"
        }), 400
    else:
        status = request.get_json().get("status")
        error = validate_status(status)
        if error:
            response = jsonify({"status": 400, "error": error}), 400
        else:
            red_flag[0]["status"] = status
            response = jsonify({
                "status": 200,
                "data": [{
                    "id": red_flag[0]["_id"],
                    "message":"Updated red-flag status"
                }]}), 200
    return response


@app.route("/api/v1/red_flags", methods=["GET"])
@token_required
@non_admin
def get_all_red_flag_records_of_given_user():
    """Get all available red flags of a given"""
    createdBy = get_current_identity()
    user_red_flags = [user_red_flags for user_red_flags
                      in red_flags if user_red_flags["createdBy"] == createdBy]
    return jsonify({
        "data": user_red_flags,
        "status": 200
    }), 200


@app.route("/api/v1/red_flags/<int:red_flag_id>", methods=["GET"])
@token_required
@non_admin
def get_single_red_flag_record_of_given_user(red_flag_id):
    """Get a red flag of a certain user with a given id"""
    createdBy = get_current_identity()

    user_red_flag = [
        user_red_flags for user_red_flags
        in red_flags if user_red_flags["createdBy"] == createdBy
        and user_red_flags["_id"] == red_flag_id]

    if not user_red_flag:
        response = jsonify({
            "status": 400,
            "error": "ID Not found. Enter a valid ID"
        }), 400
    else:
        response = jsonify({
            "data": user_red_flag,
            "status": 200
        }), 200
    return response


@app.route(
    "/api/v1/red_flags/<int:red_flag_id>/<string:what_to_edit>",
    methods=["PATCH"])
@token_required
@non_admin
def patch_red_flag_of_given_user(red_flag_id, what_to_edit):
    """Update red flag with ID(red_flag_id) of a certain user"""
    createdBy = get_current_identity()

    user_red_flag = [
        red_flag for red_flag in red_flags
        if red_flag["createdBy"] == createdBy and
        red_flag["_id"] == red_flag_id]

    red_flag_editable = [
        red_flag for red_flag in user_red_flag
        if red_flag["status"] == "draft"]

    if not request.is_json:
        response = jsonify({
            "status": 400, "error": "JSON request required"
        }), 400
    elif what_to_edit not in ["location", "comment"]:
        response = jsonify({
            "status": 404,
            "error": "Page Not found. Enter a valid URL"
        }), 404
    elif not user_red_flag:
        response = jsonify({
            "status": 400, "error": "ID Not found. Enter a valid ID"
        }), 400
    elif not red_flag_editable:
        response = jsonify({
            "status": 400,
            "error": "Only redflag in draft state can be edited"
        }), 400
    else:
        comment = request.get_json().get("comment")
        location = request.get_json().get("location")
        data = location if what_to_edit == "location" else comment
        error = validate_edit_input(data)
        if error:
            response = jsonify({"status": 400, "error": error}), 400
        else:
            red_flag_editable[0][what_to_edit] = data
            response = jsonify({
                "status": 200,
                "data": [{
                    "id": red_flag_id,
                    "message": f"Updated red-flag {what_to_edit}"
                }]}), 200
    return response


@app.route("/api/v1/red_flags/<int:red_flag_id>", methods=["DELETE"])
@token_required
@non_admin
def delete_red_flag_of_given_user(red_flag_id):
    """Delete red flag with ID(red_flag_id) of a certain user"""
    createdBy = get_current_identity()
    user_red_flag = [
        red_flag for red_flag in red_flags
        if red_flag["createdBy"] == createdBy and
        red_flag["_id"] == red_flag_id]

    red_flag_editable = [
        red_flag for red_flag in user_red_flag
        if red_flag["status"] == "draft"]

    if not user_red_flag:
        response = jsonify({
            "status": 400, "error": "ID Not found. Enter a valid ID"
        }), 400
    elif not red_flag_editable:
        response = jsonify({
            "status": 400,
            "error": "Only redflag in draft state can be deleted"
        }), 400
    else:
        print(red_flag_editable)
        red_flags.remove(red_flag_editable[0])
        response = jsonify({
            "status": 200,
            "data": [{
                "id": red_flag_id,
                "message": "Red flag record has been deleted"
            }]}), 200
    return response


@app.errorhandler(Exception)
def errors(error):
    """
    This funcion handles the 404 and 405 HTTP STATUS CODES.
    It then returns json response on a particular status code.
    """
    response = None
    if error.code == 404:
        response = jsonify({
            "status": 404,
            "error": "Page Not found. Enter a valid URL"
        }), 404
    else:
        response = jsonify({
            "status": 405,
            "error": "Method not allowed."
        }), 405
    return response
