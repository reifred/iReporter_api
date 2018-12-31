import random


class Incident:

    incident_id = 1

    def __init__(
        self, createdBy, createdOn, type, location, status, images,
            videos, comment):
        self._id = Incident.incident_id
        self.createdBy = createdBy
        self.createdOn = createdOn
        self.type = type
        self.location = location
        self.status = status
        self.images = images
        self.videos = videos
        self.comment = comment
        Incident.incident_id += 1

    def validate_input(self):
        if not self.createdBy or not isinstance(self.createdBy, int):
            return "createdBy must be an int"
        if not self.location or not isinstance(
                self.location, str) or self.location.isspace():
            return "location must not be empty string"
        if not self.status or not isinstance(
                self.status, str) or self.status.isspace():
            return "status must not be empty string"
        if not self.comment or not isinstance(
                self.comment, str) or self.comment.isspace():
            return "comment must not be empty string"
        if not self.type or not isinstance(
                self.type, str) or self.type.isspace():
            return "type must not be empty string"
        if not self.images:
            return "images must not be empty"

    @staticmethod
    def validate_location(location):
        if not location or not isinstance(location, str) or location.isspace():
            return "location must not be empty string"

    @staticmethod
    def validate_comment(comment):
        if not comment or not isinstance(comment, str) or comment.isspace():
            return "comment must not be empty string"

    def convert_to_dict(self):
        return dict(id=self._id, createdOn=self.createdOn,
                    type=self.type, location=self.location,
                    status=self.status, images=[self.images],
                    videos=[self.videos], comment=self.comment)


class User:

    user_id = 1

    def __init__(self, firstname, lastname, othernames, email, phoneNumber,
                 username, registered, isAdmin):
        self.id = id(User.user_id)
        self.firstname = firstname
        self.lastname = lastname
        self.othernames = othernames
        self.email = email
        self.phoneNumber = phoneNumber
        self.username = username
        self.registered = registered
        self.isAdmin = isAdmin
        User.user_id += 1

    def convert_to_dict(self):
        return dict(id=self.id, firstname=self.firstname,
                    lastname=self.lastname, othernames=self.othernames,
                    email=self.email, phoneNumber=self.phoneNumber,
                    username=self.username, registered=self.registered,
                    isAdmin=self.isAdmin)
