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

    def convert_to_dict(self):
        return dict(_id=self._id, createdBy=self.createdBy, 
            createdOn=self.createdOn, _type=self._type, 
            location=self.location, status=self.status, images=[self.images],
            videos=[self.videos], comment=self.comment)


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

    def convert_to_dict(self):
        return dict(_id=self._id, firstname=self.firstname,
                    lastname=self.lastname, othernames=self.othernames,
                    email=self.email, phoneNumber=self.phoneNumber,
                    username=self.username, registered=self.registered,
                    password=self.password, isAdmin=self.isAdmin)
