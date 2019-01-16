from flask import Blueprint, jsonify, request
from app.models.models import Incident
from datetime import datetime

from app.helpers.validators import(
    validate_input, validate_string, validate_comment,
    validate_user_input, validate_status)

from app.helpers.helpers import (
    token_required, get_current_identity, non_admin, admin_required
)

user_bp = Blueprint("user_bp", __name__, url_prefix="/api/v1")

red_flags = []
response = None


@user_bp.route("/")
def index():
    return "Welcome to api."


@user_bp.route("/red_flags", methods=["POST"])
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


@user_bp.route("/red_flags", methods=["GET"])
@token_required
def get_all_red_flag_records():
    """Get all available red flags of a given user"""
    red_flag_records = Incident.get_red_flags(red_flags)
    return jsonify({
        "data": red_flag_records,
        "status": 200
    }), 200


@user_bp.route("/red_flags/<int:red_flag_id>/status", methods=["PATCH"])
@token_required
@admin_required
def edit_status_of_user_red_flag(red_flag_id):
    """Edit the status of a user red flag"""
    red_flag = Incident.get_red_flag_of_id(red_flag_id,red_flags)

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


@user_bp.route("/red_flags/<int:red_flag_id>", methods=["GET"])
@token_required
def get_single_red_flag_of_id(red_flag_id):
    """Get a red flag of id red_flag_id"""
    red_flag_of_id = Incident.get_red_flag_of_id(red_flag_id, red_flags)
    if not red_flag_of_id:
        response = jsonify({
            "status": 400,
            "error": "ID Not found. Enter a valid ID"
        }), 400
    else:
        response = jsonify({
            "data": red_flag_of_id,
            "status": 200
        }), 200
    return response


@user_bp.route(
    "/red_flags/<int:red_flag_id>/<string:what_to_edit>", methods=["PATCH"])
@token_required
@non_admin
def patch_red_flag_of_given_user(red_flag_id, what_to_edit):
    """Update red flag with ID(red_flag_id) of a certain user"""
    red_flag_of_id = Incident.get_red_flag_of_id(red_flag_id, red_flags)

    if not request.is_json:
        response = jsonify({
            "status": 400, "error": "JSON request required"
        }), 400
    elif what_to_edit not in ["location", "comment"]:
        response = jsonify({
            "status": 404,
            "error": "Page Not found. Enter a valid URL"
        }), 404
    elif not red_flag_of_id:
        response = jsonify({
            "status": 400, "error": "ID Not found. Enter a valid ID"
        }), 400
    else:
        red_flag_editable = Incident.is_red_flag_editable(red_flag_id, red_flags)
        if not red_flag_editable:
            response = jsonify({
                "status": 400,
                "error": "Only redflag in draft state can be edited"
            }), 400
        else:
            comment = request.get_json().get("comment")
            location = request.get_json().get("location")
            data = location if what_to_edit == "location" else comment
            error = validate_string("location",data) if what_to_edit == "location" else validate_comment(comment)

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


@user_bp.route("/red_flags/<int:red_flag_id>", methods=["DELETE"])
@token_required
@non_admin
def delete_red_flag_of_given_user(red_flag_id):
    """Delete red flag with ID(red_flag_id) of a certain user"""
    red_flag_of_id = Incident.get_red_flag_of_id(red_flag_id, red_flags)
    if not red_flag_of_id:
        response = jsonify({
            "status": 400, "error": "ID Not found. Enter a valid ID"
        }), 400
    else:
        red_flag_editable = Incident.is_red_flag_editable(red_flag_id, red_flags)
        if not red_flag_editable:
            response = jsonify({
                "status": 400,
                "error": "Only redflag in draft state can be deleted"
            }), 400
        else:
            red_flags.remove(red_flag_editable[0])
            response = jsonify({
                "status": 200,
                "data": [{
                    "id": red_flag_id,
                    "message": "Red flag record has been deleted"
                }]}), 200
    return response