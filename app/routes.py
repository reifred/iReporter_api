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
    in the list of users
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
    This function checks whether the user exists
    before login
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
            # get the id of the current user logged in
            user_id = user[0]["_id"]
        # encode the token with user id and isAdmin status
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
    response = None
    red_flag = request.get_json()
    if not request.is_json:
        # If the request is not in JSON format then notify the user
        response = jsonify({
            "status": 400,
            "error": "JSON request required"
        }), 400
    else:
        # if the request is in JSON format then get the data
        createdOn = datetime.now().strftime("%Y-%m-%d")
        createdBy = get_current_identity()
        status = "pending"
        comment = red_flag.get("comment")
        _type = red_flag.get("_type")
        images = red_flag.get("images")
        videos = red_flag.get("videos")
        location = red_flag.get("location")

        errors = validate_input(location, comment, _type, images)

        if errors:
            # If the data contain errors then show the errors
            response = jsonify({"status": 400, "error": errors}), 400
        else:
            # If the data doesn't contain errors then store the data
            incident = Incident(createdBy, createdOn, _type, location,
                status, images, videos, comment)
            red_flags.append(incident.convert_to_dict())
            response = jsonify({
                "status": 201,
                "data":[{
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
        "Number": len(users),
        "data": users
    })


@app.route("/api/v1/red_flags/<int:red_flag_id>/status", methods=["PATCH"])
@token_required
@admin_required
def edit_status_of_user_red_flag(red_flag_id):
    """Edit the status of a user red flag"""
    response = None
    # Get all red_flags
    red_flag = [
        red_flag for red_flag in red_flags if red_flag["_id"] == red_flag_id]
    # If no red flag is got then the ID is invalid
    if not red_flag:
        response = jsonify({
            "status": 400,
            "error": "ID Not found. Enter a valid ID"
        }), 400
    else:
        # If the request is in JSON format then get the data(status)
        status = request.get_json().get("status")
    # if the ID is valid check whether the status given contain errors
        error = validate_status(status)
        if error:
            # if status contain errors notify the admin
            response = jsonify({"status": 400, "error": error}), 400
        else:
            # if there are no errors then update the status
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
    # Get current user ID
    createdBy = get_current_identity()
    # Get all red flags of the current user
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
    response = None
    # Get current user ID
    createdBy = get_current_identity()
    # Get the red flags of the current user
    user_red_flags = [
        user_red_flags for user_red_flags
        in red_flags if user_red_flags["createdBy"] == createdBy]
    # In the red flags of the current user get a redflag of a given ID
    red_flag = [
        red_flag for red_flag in user_red_flags
        if red_flag["_id"] == red_flag_id]
    # If no red flag is got then the ID is invalid
    if not red_flag:
        response = jsonify({
            "status": 400,
            "error": "ID Not found. Enter a valid ID"
        }), 400
    else:
        # if the ID is valid then show that red flag
        response = jsonify({
            "data": red_flag,
            "status": 200
        }), 200
    return response


@app.route("/api/v1/red_flags/<int:red_flag_id>/location", methods=["PATCH"])
@token_required
@non_admin
def edit_red_flag_location_of_given_user(red_flag_id):
    """Update location of red flag with ID(red_flag_id) of a certain user"""
    response = None
    # Get current user ID
    createdBy = get_current_identity()
    # if the request is not in JSON format then notify the user
    if not request.is_json:
        response = jsonify({
            "status": 400,
            "error": "JSON request required"
        }), 400
    else:
        # If the request is in JSON format then get the data(location)
        location = request.get_json().get("location")
    # Get the red flags of the current user
        user_red_flags = [
            user_red_flags for user_red_flags
            in red_flags if user_red_flags["createdBy"] == createdBy]
    # In the red flags of the current user get a redflag of a given ID
        red_flag = [
            red_flag for red_flag in user_red_flags
            if red_flag["_id"] == red_flag_id]
    # If no red flag is got then the ID is invalid
        if not red_flag:
            response = jsonify({
                "status": 400,
                "error": "ID Not found. Enter a valid ID"
            }), 400
        else:
            # if the ID is valid check whether the location given contain
            # errors
            error = validate_location(location)
            if error:
                # if location contain errors notify the user
                response = jsonify({"status": 400, "error": error}), 400
            else:
                # if there are no errors then update the location
                red_flag[0]["location"] = location
                response = jsonify({
                    "status": 200,
                    "data": [{
                        "id": red_flag[0]["_id"],
                        "message":"Updated red-flag location"
                    }]}), 200
    return response


@app.route("/api/v1/red_flags/<int:red_flag_id>/comment", methods=["PATCH"])
@token_required
@non_admin
def patch_red_flag_comment_of_given_user(red_flag_id):
    """Update comment of red flag with ID(red_flag_id) of a certain user"""
    response = None
    # Get current user ID
    createdBy = get_current_identity()
    # if the request is not in JSON format then notify the user
    if not request.is_json:
        response = jsonify({
            "status": 400, "error": "JSON request required"
        }), 400
    else:
        # If the request is in JSON format then get the data(comment)
        comment = request.get_json().get("comment")
    # Get the red flags of the current user
        user_red_flags = [
            user_red_flags for user_red_flags
            in red_flags if user_red_flags["createdBy"] == createdBy]
    # In the red flags of the current user get a redflag of a given ID
        incident = [
            red_flag for red_flag in user_red_flags
            if red_flag["_id"] == red_flag_id]
        if not incident:
            # If no red flag is got then the ID is invalid
            response = jsonify({
                "status": 400, "error": "ID Not found. Enter a valid ID"
            }), 400
        else:
            # if the ID is valid check whether the location given contain
            # errors
            error = validate_comment(comment)
            if error:
                # if location contain errors notify the user
                response = jsonify({"status": 400, "error": error}), 400
            else:
                # if there are no errors then update the location
                incident[-1]["comment"] = comment
                response = jsonify({
                    "status": 200,
                    "data": [{
                        "id": incident[-1]["_id"],
                        "message":"Updated red-flag comment"
                    }]}), 200
    return response


@app.route("/api/v1/red_flags/<int:red_flag_id>", methods=["DELETE"])
@token_required
@non_admin
def delete_red_flag_of_given_user(red_flag_id):
    """Delete red flag with ID(red_flag_id) of a certain user"""
    response = None
    # Get current user ID
    createdBy = get_current_identity()
    # if the request is not in JSON format then notify the user
    red_flag = [
        red_flag for red_flag in red_flags if red_flag["_id"] == red_flag_id]
    if not red_flag:
        response = jsonify({
            "status": 400, "error": "ID Not found. Enter a valid ID"
        }), 400
    else:
        # If request in JSON FORMAT get the red flags of the current user
        user_red_flags = [
            user_red_flags for user_red_flags
            in red_flags if user_red_flags["createdBy"] == createdBy]
        print(user_red_flags)
    # In the red flags of the current user get a redflag of a given ID
        red_flag = [
            red_flag for red_flag in user_red_flags
            if red_flag["_id"] == red_flag_id]
        if not red_flag:
            response = jsonify({
                "status": 400, "error": "ID Not found. Enter a valid ID"
            }), 400
        else:
            # Delete a redflag of ID(red_flag_id)
            print(red_flag)
            red_flags.remove(red_flag[0])
            response = jsonify({
                "status": 200,
                "data": [{
                    "id": red_flag[0]["_id"],
                    "message":"Red flag record has been deleted"
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
