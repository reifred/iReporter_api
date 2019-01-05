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

@app.route("/api/v1/red_flags", methods=["POST"])
@token_required
@non_admin
def create_red_flag_record_of_given_user():
    """Create a red flag of a given user"""
    response = None
    red_flag = request.get_json()
    if not request.is_json:
        response = jsonify({
            "status": 400,
            "error": "JSON request required"
        }), 400
    else:
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
            response = jsonify({"status": 400, "error": errors}), 400
        else:
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
