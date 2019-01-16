import re

""" Validations for red flag input"""

def validate_string(string_key, string_value):
    if not string_value or not isinstance(
            string_value, str) or string_value.isspace():
        return f"{string_key} should not be empty string"


def validate_type(_type):
    if not _type or not isinstance(
            _type, str) or _type.isspace():
        return "_type must not be empty string"
    if _type not in ["red-flag", "intervention"]:
        return "given _type not allowed"

def validate_images(images):
    if not images:
        return "images must not be empty"


def validate_comment(comment):
    if not comment or not isinstance(
            comment, str) or comment.isspace():
        return "comment must not be empty string"
    if len(comment) not in range(10, 40):
        return "comment must be atleast 10 to 40 characters"

def validate_input(location, comment, _type, images):
    error = {}
    error["location"] = validate_string("location",location)
    error["comment"] = validate_comment(comment)
    error["_type"] = validate_type(_type)
    error["images"] = validate_images(images)
    error_list = [value for key, value in error.items() if value]
    first_error = "".join(error_list[0]) if error_list else None
    return first_error


def validate_status(status):
    if not status or not isinstance(status, str) or status.isspace():
        return "status must not be empty string"
    elif status not in ["resolved", "under investigation", "rejected"]:
        return "given status not allowed"


""" Validations for user input"""

def validate_email(email):
    if not email or not isinstance(
            email, str) or email.isspace():
        return "email shoud not be empty string"
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "invalid email syntax"


def validate_password(password):
    if not password or not isinstance(
        password, str) or password.isspace():
        return "password shoud not be empty string"
    elif len(password) not in range(6, 16):
        return "password length should be between 6 to 16"
    elif(
        not re.search("[A-Z]", password) or
        not re.search("[a-z]", password) or
        not re.search("[0-9]", password)):
        return "password must have upper and lower character plus number"


def validate_user_input(
        firstname, lastname, email, phoneNumber, username, password):
        error = {}
        error["firstname"] = validate_string("firstname", firstname)
        error["lastname"] = validate_string("lastname", lastname)
        error["email"] = validate_email(email)
        error["phoneNumber"] = validate_string("phoneNumber", phoneNumber)
        error["username"] = validate_string("username", username)
        error["password"] = validate_password(password)
        error_list = [value for key, value in error.items() if value]
        first_error = "".join(error_list[0]) if error_list else None
        return first_error

def validate_sign_in(username, password):
        error = {}
        error["username"] = validate_string("username", username)
        error["password"] = validate_password(password)
        error_list = [value for key, value in error.items() if value]
        first_error = "".join(error_list[0]) if error_list else None
        return first_error