from app.routes import app
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
            "password": "password",
            "isAdmin": 0
            }
        response = app.test_client().post('/api/v1/auth/sign_up', json=user)
        user = {
            "username": "username33",
            "password": "password",
            "isAdmin": 0
        }
        response = app.test_client().post('/api/v1/auth/sign_in', json=user)
        token = json.loads(response.data)['token']
        print(token)
        return token
    
    @staticmethod
    def get_admin_token():
        user = {
            "username": "admin",
            "password": "adminpass",
            "isAdmin": 1
        }
        response = app.test_client().post('/api/v1/auth/sign_in', json=user)
        token = json.loads(response.data)['token']
        print(token)
        return token