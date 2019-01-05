from app.routes import app
import unittest
import json


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client(self)
        self.user = {
            "firstname": "Mugerwa",
            "lastname": "Fred",
            "othernames": "",
            "email": "rei33@gmail.com",
            "phoneNumber": "0757605424",
            "username": "username",
            "password": "password",
            "isAdmin": 0
            }

    def test_1_home(self):
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        self.assertIn("Welcome to api", str(response.data))

    def test_2_wrong_url(self):
        user={}
        response = self.client.post("/api/v1/auth/sign_in/fred", json=user)
        json_data = json.loads(response.data)
        self.assertEqual(404,response.status_code)
        self.assertEqual(
            json_data["error"],
            "Page Not found. Enter a valid URL")

    def test_3_sign_in_without_registering(self):
        user = {}
        response = self.client.post("/api/v1/auth/sign_in", json=user)
        json_data = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(json_data["error"], "User doesnt exist")
    
    def test_4_sign_up_with_short_password(self):
        user = {
            "firstname": "Mugerwa",
            "lastname": "Fred",
            "othernames": "",
            "email": "fred@gmail.com",
            "phoneNumber": "0757605424",
            "username": "username",
            "password": "pass",
            "isAdmin": 0
            }
        response = self.client.post("/api/v1/auth/sign_up", json=user)
        json_data = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            json_data["error"], 
            "password length should be between 6 to 10")

    def test_4_sign_up_without_data(self):
        user = {}
        response = self.client.post("/api/v1/auth/sign_up", json=user)
        json_data = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            json_data["error"], 
            "firstname shoud not be empty string")

    def test_5_sign_up_with_correct_data(self):
        response = self.client.post("/api/v1/auth/sign_up", json=self.user)
        json_data = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(
            json_data["data"][0]["message"], 
            "User registered")
    
    def test_6_sign_up_with_same_username_or_email(self):
        response = self.client.post("/api/v1/auth/sign_up", json=self.user)
        json_data = json.loads(response.data)
        self.assertEqual(400,response.status_code)
        self.assertEqual(json_data["error"],"username or email already exists")

    def test_7_sign_in_after_registering(self):
        user = {
            "username": "username",
            "password": "password",
            "isAdmin": 0
        }
        response = self.client.post("/api/v1/auth/sign_in", json=user)
        json_data = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(json_data["message"], "User login")

    def test_8_sign_up_with_wrong_data_type(self):
        user = {
            "firstname": "Mugerwa",
            "lastname": 11111,
            "othernames": "",
            "email": "mugerwafred@gmail.com",
            "phoneNumber": "0757605424",
            "username": "username2",
            "password": "password",
            "isAdmin": 0
            }
        response = self.client.post("/api/v1/auth/sign_up", json=user)
        json_data = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            json_data["error"], "lastname shoud not be empty string")

    def test_9_sign_up_with_wrong_email(self):
        user = {
            "firstname": "Mugerwa",
            "lastname": "Fred",
            "othernames": "",
            "email": "email",
            "phoneNumber": "0757605424",
            "username": "username2",
            "password": "password",
            "isAdmin": 0
            }
        response = self.client.post("/api/v1/auth/sign_up", json=user)
        json_data = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            json_data["error"], "invalid email syntax")
