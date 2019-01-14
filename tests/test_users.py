from app import app
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

    def test_01_home(self):
        response = self.client.get("/api/v1/")
        self.assertEqual(200, response.status_code)
        self.assertIn("Welcome to api", str(response.data))

    def test_02_sign_up_without_JSON(self):
        response = self.client.post("/api/v1/auth/sign_up")
        self.assertEqual(400, response.status_code)

    def test_03_sign_in_without_JSON(self):
        response = self.client.post("/api/v1/auth/sign_in")
        self.assertEqual(400, response.status_code)

    def test_04_sign_in_without_registering(self):
        response = self.client.post("/api/v1/auth/sign_in", json={})
        json_data = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            json_data["error"], 
            "username shoud not be empty string"
        )

    def test_05_sign_up_with_short_password(self):
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
            "password length should be between 6 to 16")

    def test_06_sign_up_without_data(self):
        response = self.client.post("/api/v1/auth/sign_up", json={})
        json_data = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            json_data["error"],
            "firstname shoud not be empty string")

    def test_07_sign_up_with_correct_data(self):
        response = self.client.post("/api/v1/auth/sign_up", json=self.user)
        json_data = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(
            json_data["data"][0]["message"],
            "User registered")

    def test_08_sign_up_with_same_username_or_email(self):
        response = self.client.post("/api/v1/auth/sign_up", json=self.user)
        json_data = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            json_data["error"],
            "username or email already exists")

    def test_09_sign_in_after_registering(self):
        user = {
            "username": "username",
            "password": "password",
            "isAdmin": 0
        }
        response = self.client.post("/api/v1/auth/sign_in", json=user)
        json_data = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(json_data["data"][0]["message"], "User login")

    def test_10_sign_in_with_wrong_username(self):
        user = {
            "username": "usern",
            "password": "password",
            "isAdmin": 0
        }
        response = self.client.post("/api/v1/auth/sign_in", json=user)
        json_data = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(json_data["error"], "User doesnt exist")

    def test_11_sign_up_with_wrong_data_type(self):
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

    def test_12_sign_up_with_wrong_email(self):
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