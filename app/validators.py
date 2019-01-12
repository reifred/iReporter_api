import re


def validate_input(location, comment, _type, images):
    if not location or not isinstance(
            location, str) or location.isspace():
        return "location must not be empty string"
    if not comment or not isinstance(
            comment, str) or comment.isspace():
        return "comment must not be empty string"
    if len(comment) not in range(8, 40):
        return "comment must be atleast 5 to 40 characters"
    if not _type or not isinstance(
            _type, str) or _type.isspace():
        return "_type must not be empty string"
    if _type not in ["red-flag", "intervention"]:
        return "given _type not allowed"
    if not images:
        return "images must not be empty"


def validate_edit_input(data):
    if not data or not isinstance(data, str) or data.isspace():
        return "Input must not be empty string"


def validate_status(status):
    if not status or not isinstance(status, str) or status.isspace():
        return "status must not be empty string"
    elif status not in ["resolved", "under investigation", "rejected"]:
        return "given status not allowed"


def validate_user_input(
        firstname, lastname, email, phoneNumber, username, password):
    if not firstname or not isinstance(
            firstname, str) or firstname.isspace():
        return "firstname shoud not be empty string"
    if not lastname or not isinstance(
            lastname, str) or lastname.isspace():
        return "lastname shoud not be empty string"
    if not email or not isinstance(
            email, str) or email.isspace():
        return "email shoud not be empty string"
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "invalid email syntax"
    if not phoneNumber or not isinstance(
            phoneNumber, str) or phoneNumber.isspace():
        return "phoneNumber shoud not be empty string"
    if not username or not isinstance(
            username, str) or username.isspace():
        return "username shoud not be empty string"
    if not password or not isinstance(
            password, str) or password.isspace():
        return "password shoud not be empty string"
    if len(password) not in range(6, 16):
        return "password length should be between 6 to 16"


def validate_sign_in(username, password):
    if not username or not isinstance(
            username, str) or username.isspace():
        return "username shoud not be empty string"
    if not password or not isinstance(
            password, str) or password.isspace():
        return "password shoud not be empty string"
    if len(password) not in range(6, 16):
        return "password length should be between 6 to 16"
