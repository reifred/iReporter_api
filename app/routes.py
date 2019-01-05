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

@app.route("/api/v1/red_flags/<int:red_flag_id>", methods=["DELETE"])
@token_required
@non_admin
def delete_red_flag_of_given_user(red_flag_id):
    """Delete red flag with ID(red_flag_id) of a certain user"""
    response = None
    createdBy = get_current_identity()
    red_flag = [
        red_flag for red_flag in red_flags if red_flag["_id"] == red_flag_id]
    if not red_flag:
        response = jsonify({
            "status": 400, "error": "ID Not found. Enter a valid ID"
        }), 400
    else:
        user_red_flags = [
            user_red_flags for user_red_flags
            in red_flags if user_red_flags["createdBy"] == createdBy]
        print(user_red_flags)
        red_flag = [
            red_flag for red_flag in user_red_flags
            if red_flag["_id"] == red_flag_id]
        if not red_flag:
            response = jsonify({
                "status": 400, "error": "ID Not found. Enter a valid ID"
            }), 400
        else:
            print(red_flag)
            red_flags.remove(red_flag[0])
            response = jsonify({
                "status": 200,
                "data": [{
                    "id": red_flag[0]["_id"],
                    "message":"Red flag record has been deleted"
                }]}), 200
    return response
