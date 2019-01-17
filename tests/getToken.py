from app import app
import json


class GetToken:

    @staticmethod
    def get_user_token():
        user = {
            "firstname": "Mugerwa",
            "lastname": "Fred",
            "othernames": "",
            "email": "reifred33@gmail.com",
            "phoneNumber": "0757605424",
            "username": "username33",
            "password": "Password33",
            "isAdmin": False
        }
        response = app.test_client().post('/api/v1/auth/sign_up', json=user)
        user = {
            "username": "username33",
            "password": "Password33",
            "isAdmin": False
        }
        response = app.test_client().post('/api/v1/auth/sign_in', json=user)
        token = json.loads(response.data)["data"][0]['token']
        return token

    @staticmethod
    def get_admin_token():
        user = {
            "username": "admin",
            "password": "admin@33",
            "isAdmin": True
        }
        response = app.test_client().post('/api/v1/auth/sign_in', json=user)
        token = json.loads(response.data)["data"][0]['token']
        return token
