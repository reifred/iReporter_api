from app.routes import app
from app.models import Incident, User
from tests.getToken import GetToken
import unittest
import json


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client(self)
        self.red_flag = {
            "comment": "We are facing this challenge",
            "_type": "draft",
            "images": "pic.jpg",
            "location": "Lat 1231 Long 1424",
            "status": "red-flag",
            "videos": "vid.mp4"
        }

    def test_01_create_red_flag_without_token(self):
        response = self.client.post(
            "/api/v1/red_flags", json=self.red_flag)
        json_data = json.loads(response.data)
        self.assertEqual(401, response.status_code)
        self.assertEqual(json_data["error"], "Invalid token")

    def test_02_user_create_red_flag(self):
        response = self.client.post(
            "/api/v1/red_flags",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()),
            json=self.red_flag)
        json_data = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(
            json_data["message"],
            "Created red-flag record")

    def test_03_admin_create_red_flag(self):
        response = self.client.post(
            "/api/v1/red_flags",
            headers=dict(
                Authorization='Bearer ' + GetToken.get_admin_token()),
            json=self.red_flag)
        json_data = json.loads(response.data)
        self.assertEqual(403, response.status_code)
        self.assertEqual(
            json_data["error"],
            "Admin cannot access this resource")

    def test_04_admin_get_all_users_red_flags(self):
        response = self.client.get(
            "/api/v1/auth/red_flags",
            headers=dict(
                Authorization='Bearer ' + GetToken.get_admin_token()))
        json_data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertIn("data", json_data)

    def test_05_user_get_all_users_red_flags(self):
        response = self.client.get(
            "/api/v1/auth/red_flags",
            headers=dict(
                Authorization='Bearer ' + GetToken.get_user_token()))
        json_data = json.loads(response.data)
        self.assertEqual(403, response.status_code)
        self.assertEqual(
            json_data["error"],
            "Only Admin can access this resource")

    def test_06_get_user_red_flags_without_token(self):
        response = self.client.get("/api/v1/red_flags")
        json_data = json.loads(response.data)
        self.assertEqual(401, response.status_code)
        self.assertEqual(json_data["error"], "Invalid token")

    def test_07_get_user_red_flags(self):
        response = self.client.get(
            "/api/v1/red_flags",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()),
            json=self.red_flag)
        self.assertEqual(200, response.status_code)

    def test_08_get_user_single_red_flags_without_token(self):
        response = self.client.get("/api/v1/red_flags/1")
        json_data = json.loads(response.data)
        self.assertEqual(401, response.status_code)
        self.assertEqual(json_data["error"], "Invalid token")

    def test_09_get_user_single_red_flag(self):
        response = self.client.get(
            "/api/v1/red_flags/1",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()),
            json=self.red_flag)
        json_data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            json_data["data"][0]["comment"], "We are facing this challenge")

    def test_10_edit_user_red_flag_location_without_token(self):
        location = {"location": "Kampala"}
        response = self.client.patch(
            "/api/v1/red_flags/1/location", json=location)
        json_data = json.loads(response.data)
        self.assertEqual(401, response.status_code)
        self.assertEqual(json_data["error"], "Invalid token")

    def test_11_edit_user_red_flag_location(self):
        location = {"location": "Kampala"}
        response = self.client.patch(
            "/api/v1/red_flags/1/location",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()),
            json=location)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json_data["data"][0]["message"], "Updated red-flag location")

    def test_12_admin_edit_user_red_flag_location(self):
        location = {"location": "Kampala"}
        response = self.client.patch(
            "/api/v1/red_flags/1/location",
            headers=dict(
                Authorization='Bearer ' + GetToken.get_admin_token()),
            json=location)
        json_data = json.loads(response.data)
        self.assertEqual(403, response.status_code)
        self.assertEqual(
            json_data["error"],
            "Admin cannot access this resource")

    def test_13_edit_user_red_flag_location_without_data(self):
        response = self.client.patch(
            "/api/v1/red_flags/1/location",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()))
        self.assertEqual(response.status_code, 400)
        json_data = json.loads(response.data)
        self.assertEqual(
            json_data["error"], "JSON request required")

    def test_14_edit_user_red_flag_location_with_wrong_url(self):
        response = self.client.patch(
            "/api/v1/red_flags/1/location///",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()))
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(
            json_data["error"], "Page Not found. Enter a valid URL")

    def test_15_edit_user_red_flag_comment(self):
        comment = {"comment": "New comment"}
        response = self.client.patch(
            "/api/v1/red_flags/1/comment",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()),
            json=comment)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json_data["data"][0]["message"], "Updated red-flag comment")

    def test_16_edit_user_red_flag_comment_without_token(self):
        comment = {"comment": "New comment"}
        response = self.client.patch(
            "/api/v1/red_flags/1/comment", json=comment)
        json_data = json.loads(response.data)
        self.assertEqual(401, response.status_code)
        self.assertEqual(json_data["error"], "Invalid token")

    def test_17_admin_edit_user_red_flag_comment(self):
        comment = {"comment": "New comment"}
        response = self.client.patch(
            "/api/v1/red_flags/1/comment",
            headers=dict(
                Authorization='Bearer ' + GetToken.get_admin_token()),
            json=comment)
        json_data = json.loads(response.data)
        self.assertEqual(403, response.status_code)
        self.assertEqual(
            json_data["error"],
            "Admin cannot access this resource")

    def test_18_edit_user_red_flag_comment_without_data(self):
        response = self.client.patch(
            "/api/v1/red_flags/1/comment",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()))
        self.assertEqual(response.status_code, 400)
        json_data = json.loads(response.data)
        self.assertEqual(
            json_data["error"], "JSON request required")

    def test_19_edit_user_red_flag_comment_with_wrong_ID(self):
        comment = {"comment": "New comment"}
        response = self.client.patch(
            "/api/v1/red_flags/11/comment",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()),
            json=comment)
        self.assertEqual(response.status_code, 400)
        json_data = json.loads(response.data)
        self.assertEqual(
            json_data["error"], "ID Not found. Enter a valid ID")

    def test_20_edit_user_red_flag_comment_with_wrong_data_type(self):
        comment = {"comment": 1233}
        response = self.client.patch(
            "/api/v1/red_flags/1/comment",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()),
            json=comment)
        json_data = json.loads(response.data)
        self.assertEqual(
            json_data["error"],
            "comment must not be empty string")

    def test_21_admin_edit_user_red_flag_status(self):
        status = {"status": "draft"}
        response = self.client.patch(
            "/api/v1/red_flags/1/status",
            headers=dict(Authorization='Bearer ' + GetToken.get_admin_token()),
            json=status)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json_data["data"][0]["message"], "Updated red-flag status")

    def test_22_admin_edit_user_red_flag_status_with_wrong_data(self):
        status = {"status": "draf"}
        response = self.client.patch(
            "/api/v1/red_flags/1/status",
            headers=dict(Authorization='Bearer ' + GetToken.get_admin_token()),
            json=status)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_data["error"], "given status not allowed")

    def test_23_admin_edit_user_red_flag_status_with_wrong_data(self):
        status = {"status": 34343}
        response = self.client.patch(
            "/api/v1/red_flags/1/status",
            headers=dict(Authorization='Bearer ' + GetToken.get_admin_token()),
            json=status)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_data["error"], "status must not be empty string")

    def test_24_user_edit_user_red_flag_status(self):
        status = {"status": "draft"}
        response = self.client.patch(
            "/api/v1/red_flags/1/status",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()),
            json=status)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            json_data["error"],
            "Only Admin can access this resource")

    def test_25_remove_user_red_flag(self):
        response = self.client.delete(
            "/api/v1/red_flags/1",
            headers=dict(
                Authorization='Bearer ' +
                GetToken.get_user_token()))
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json_data["data"][0]["message"],
            "Red flag record has been deleted")

    def test_26_remove_user_red_flag_with_wrong_data(self):
        response = self.client.delete(
            "/api/v1/red_flags/10",
            headers=dict(
                Authorization='Bearer ' +
                GetToken.get_user_token()))
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_data["error"], "ID Not found. Enter a valid ID")

    def test_27_admin_remove_user_red_flag(self):
        response = self.client.delete(
            "/api/v1/red_flags/1",
            headers=dict(
                Authorization='Bearer ' + GetToken.get_admin_token()))
        json_data = json.loads(response.data)
        self.assertEqual(403, response.status_code)
        self.assertEqual(
            json_data["error"],
            "Admin cannot access this resource")

    def test_28_method_not_allowed(self):
        response = self.client.delete("/api/v1/red_flags")
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            json_data["error"], "Method not allowed.")

    def test_29_admin_get_all_registered_users(self):
        response = self.client.get(
            "/api/v1/users",
            headers=dict(
                Authorization='Bearer ' + GetToken.get_admin_token()))
        self.assertEqual(200, response.status_code)

    def test_30_user_get_all_registered_users(self):
        response = self.client.get(
            "/api/v1/users",
            headers=dict(
                Authorization='Bearer ' + GetToken.get_user_token()))
        self.assertEqual(403, response.status_code)

    def test_31_user_create_red_flag_without_data(self):
        response = self.client.post(
            "/api/v1/red_flags",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()),
            json={})
        self.assertEqual(400, response.status_code)

    def test_32_user_create_red_flag_with_wrong_ID(self):
        response = self.client.get(
            "/api/v1/red_flags/70",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()))
        self.assertEqual(400, response.status_code)

    def test_32_admin_edit_red_flag_status_with_wrong_ID(self):
        response = self.client.patch(
            "/api/v1/red_flags/70/status",
            headers=dict(Authorization='Bearer ' + GetToken.get_admin_token()))
        self.assertEqual(400, response.status_code)

    def test_33_admin_get_all_registered_users_with_wrong_url(self):
        response = self.client.get(
            "/api/v1/users/as",
            headers=dict(
                Authorization='Bearer ' + GetToken.get_admin_token()))
        self.assertEqual(404, response.status_code)
