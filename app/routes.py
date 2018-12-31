from flask import Flask, jsonify, make_response, request
from app.models import Incident
from datetime import datetime

app = Flask(__name__)

red_flags = []


@app.route("/")
def index():
    return "Welcome to api."


@app.route("/api/v1/red_flags", methods=["GET"])
def get_all_red_flag_records():
    """Get all available red flags"""
    return jsonify({
        "data": red_flags,
        "status": 200
    }), 200


@app.route("/api/v1/red_flags/<int:red_flag_id>", methods=["GET"])
def get_single_red_flag_record(red_flag_id):
    """Get a red flag with a given id"""
    red_flag = [
        red_flag for red_flag in red_flags if red_flag["id"] == red_flag_id]
    if not red_flag:
        return jsonify({
            "status": 400,
            "error": "ID Not found. Enter a valid ID"
        }), 400
    return jsonify({
        "data": red_flag,
        "status": 200
    }), 200


@app.route("/api/v1/red_flags", methods=["POST"])
def create_red_flag_record():
    """Create a red flag"""
    red_flag = request.get_json()
    if not request.is_json:
        return jsonify({
            "status": 400,
            "error": "JSON request required"
        }), 400
    createdOn = datetime.now().strftime("%Y-%m-%d")
    createdBy = red_flag.get("createdBy")
    status = red_flag.get("status")
    comment = red_flag.get("comment")
    type = red_flag.get("type")
    images = red_flag.get("images")
    videos = red_flag.get("videos")
    location = red_flag.get("location")

    incident = Incident(
        createdBy, createdOn, type, location, status, images, videos, comment)
    errors = incident.validate_input()
    if errors:
        return jsonify({"status": 400, "error": errors}), 400

    red_flags.append(incident.convert_to_dict())

    return jsonify({
        "status": 201,
        "data": [{
            "id": incident._id,
            "message": "Created red-flag record"}]
    }), 201


@app.route("/api/v1/red_flags/<int:red_flag_id>/location", methods=["PATCH"])
def edit_red_flag_location(red_flag_id):
    if not request.is_json:
        return jsonify({
            "status": 400,
            "error": "JSON request required"
        }), 400
    location = request.get_json().get("location")
    red_flag = [
        red_flag for red_flag in red_flags if red_flag["id"] == red_flag_id]
    if not red_flag:
        return jsonify({
            "status": 400,
            "error": "ID Not found. Enter a valid ID"
        }), 400
    error = Incident.validate_location(location)
    if error:
        return jsonify({"status": 400, "error": error}), 400
    red_flag[0]["location"] = location
    return jsonify({
        "status": 200,
        "data": [{
            "id": red_flag[0]["id"],
            "message":"Updated red-flag location"
        }]}), 200


@app.route("/api/v1/red_flags/<int:red_flag_id>/comment", methods=["PATCH"])
def patch_red_flag_comment(red_flag_id):
    if not request.is_json:
        return jsonify({
            "status": 400, "error": "JSON request required"
        }), 400
    comment = request.get_json().get("comment")
    incident = [
        incident for incident in red_flags if incident["id"] == red_flag_id]
    if not incident:
        return jsonify({
            "status": 400, "error": "ID Not found. Enter a valid ID"
        }), 400
    error = Incident.validate_comment(comment)
    if error:
        return jsonify({"status": 400, "error": error}), 400
    incident[-1]["comment"] = comment
    return jsonify({
        "status": 200,
        "data": [{
            "id": incident[-1]["id"],
            "message":"Updated red-flag comment"
        }]}), 200


@app.route("/api/v1/red_flags/<int:red_flag_id>", methods=["DELETE"])
def delete_red_flag(red_flag_id):
    red_flag = [
        red_flag for red_flag in red_flags if red_flag["id"] == red_flag_id]
    if not red_flag:
        return jsonify({
            "status": 400, "error": "ID Not found. Enter a valid ID"
        }), 400
    red_flags.remove(red_flag[0])
    return jsonify({
        "status": 200,
        "data": [{
            "id": red_flag[0]["id"],
            "message":"Red flag record has been deleted"
        }]}), 200


@app.errorhandler(Exception)
def errors(error):
    """
    This funcion handles the 404 and 405 HTTP STATUS CODES.
    It then returns json response on a particular status code.
    """
    if error.code == 404:
        return jsonify({
            "status": 404,
            "error": "Page Not found. Enter a valid URL"
        }), 404
    else:
        return jsonify({
            "status": 405,
            "error": "Method not allowed. Check your HTTP METHOD"
        }), 405
