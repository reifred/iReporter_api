from werkzeug.security import generate_password_hash, check_password_hash
from app.helpers.helpers import get_current_role, get_current_identity


class Incident:

    incident_id = 1

    def __init__(
        self, createdBy, createdOn, _type, location, status, images,
            videos, comment):
        self._id = Incident.incident_id
        self.createdBy = createdBy
        self.createdOn = createdOn
        self._type = _type
        self.location = location
        self.status = status
        self.images = images
        self.videos = videos
        self.comment = comment
        Incident.incident_id += 1

    @staticmethod
    def red_flag_exists(createdBy, comment, location, redflag_list):
        red_flag = [
            red_flag for red_flag in redflag_list 
            if red_flag["createdBy"] == createdBy and 
            red_flag["comment"] == comment and 
            red_flag["location"] == location ]
        return red_flag

    @staticmethod
    def get_red_flag_of_id(red_flag_id, red_flags):
        red_flag_of_id = [
            red_flag for red_flag in red_flags
            if red_flag["_id"] == red_flag_id]

        if not get_current_role():
            red_flag_of_id = [
                red_flag for red_flag in red_flags
                if red_flag["createdBy"] == get_current_identity()
                and red_flag["_id"] == red_flag_id]
        return red_flag_of_id

    @staticmethod
    def get_red_flags(red_flags_list):
        red_flags = red_flags_list

        if not get_current_role():
            red_flags = [
                red_flag for red_flag in red_flags
                if red_flag["createdBy"] == get_current_identity()]
        return red_flags

    @staticmethod
    def is_red_flag_editable(red_flag_id, red_flags):
        red_flag_of_id = Incident.get_red_flag_of_id(red_flag_id, red_flags)
        if red_flag_of_id[0]["status"] == "draft":
            return red_flag_of_id

    def convert_to_dict(self):
        return dict(_id=self._id, createdBy=self.createdBy,
                    createdOn=self.createdOn, _type=self._type,
                    location=self.location, status=self.status,
                    images=[self.images], videos=[self.videos],
                    comment=self.comment)


class User:

    user_id = 1

    def __init__(self, firstname, lastname, othernames, email, phoneNumber,
                 username, password, registered, isAdmin):
        self._id = User.user_id
        self.firstname = firstname
        self.lastname = lastname
        self.othernames = othernames
        self.email = email
        self.phoneNumber = phoneNumber
        self.username = username
        self.password = password
        self.registered = registered
        self.isAdmin = isAdmin
        User.user_id += 1

    @staticmethod
    def username_exists(name, users):
        username = [
            username for username in users if username["username"] == name]
        return username

    @staticmethod
    def verify_user(data_input, users_list, username, password, isAdmin):
        user = [data_input for data_input in users_list
                if data_input["username"] == username and
                check_password_hash(data_input["password"], password) and
                data_input["isAdmin"] == isAdmin]
        return user

    @staticmethod
    def user_exits(user_list, username, email):
        user = [user for user in user_list if user["username"] == username
                or user["email"] == email]
        return user

    def convert_to_dict(self):
        return dict(_id=self._id, firstname=self.firstname,
                    lastname=self.lastname, othernames=self.othernames,
                    email=self.email, phoneNumber=self.phoneNumber,
                    username=self.username, registered=self.registered,
                    password=self.password, isAdmin=self.isAdmin)
