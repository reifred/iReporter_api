from functools import wraps
from os import environ
from flask import request, jsonify
import jwt
import datetime
from app.models import User

secret_key = environ.get("SECRET_KEY", "my_secret_key")


def encode_token(user_id, isAdmin=0):
    """
    Function returns encoded token 
    that contains uid,admin,iat,exp
    """
    payload = {
        "uid": user_id,
        "adm": isAdmin,
        "iat": datetime.datetime.utcnow(),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=3)
    }
    token = jwt.encode(payload, secret_key, algorithm="HS256").decode("utf-8")
    return token

def decoded_token(token):
    """
    Function returns decoded token 
    {uid: 1, "adm: 0, iat: 1212121, ext: 4757575"}
    """
    decoded = jwt.decode(str(token), secret_key, algorithms="HS256")
    return decoded

def extract_token_from_header():
    authorization_header = request.headers.get("Authorization")
    if not authorization_header or "Bearer" not in authorization_header:
        return jsonify({
            "error" : "Bad authorization header",
            "status" : 400
        })
    token = str(authorization_header).split(" ")[1]
    return token

def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        response = None
        try:
            token = extract_token_from_header()
            decoded_token(token)
            response = func(*args, **kwargs)
        except jwt.ExpiredSignatureError:
            response = jsonify({
                "error" : "Your token expired",
                "status" : 401
            }), 401
        except jwt.InvalidTokenError:
            response = jsonify({
                "error" : "Invalid token",
                "status" : 401
            }), 401
        return response
    return wrapper

def get_current_identity():
    return decoded_token(extract_token_from_header())["uid"]

def get_current_role():
    return decoded_token(extract_token_from_header())["adm"]

def non_admin(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if get_current_role():
            return jsonify({
                "error" : "Admin cannot access this resource",
                "status" : 403
            }), 403
        return func(*args, **kwargs)
    return wrapper

def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not get_current_role():
            return jsonify({
                "error" : "Only Admin can access this resource",
                "status" : 403
            }), 403
        return func(*args, **kwargs)
    return wrapper
