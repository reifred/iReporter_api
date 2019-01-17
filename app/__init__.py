from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from app.routes.users import user_bp
from app.routes.auth import auth_bp

app = Flask(__name__)
CORS(app)
app.register_blueprint(user_bp)
app.register_blueprint(auth_bp)


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
    