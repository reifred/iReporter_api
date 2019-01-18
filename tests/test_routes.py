from app import app
from tests.getToken import GetToken
import unittest
import json


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client(self)
        self.red_flag = {
            "comment": "We are facing this challenge",
            "_type": "red-flag",
            "images": "pic.jpg",
            "location": "Lat 1231 Long 1424",
            "videos": "vid.mp4"
        }

    def test_01_create_red_flag_without_JSON_data(self):
        response = self.client.post(
            "/api/v1/red_flags",
            headers=dict(
                Authorization='Bearer ' +
                GetToken.get_user_token()))
        json_data = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            json_data["error"], "JSON request required")

    def test_02_create_red_flag_without_token(self):
        response = self.client.post(
            "/api/v1/red_flags", json=self.red_flag)
        json_data = json.loads(response.data)
        self.assertEqual(401, response.status_code)
        self.assertEqual(json_data["error"], "Invalid token")

    def test_03_user_create_red_flag(self):
        response = self.client.post(
            "/api/v1/red_flags",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()),
            json=self.red_flag)
        json_data = json.loads(response.data)
        self.assertEqual(201, response.status_code)
        self.assertEqual(
            json_data["data"][0]["message"], "Created red-flag record")

    def test_03_user_recreate_red_flag(self):
        response = self.client.post(
            "/api/v1/red_flags",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()),
            json=self.red_flag)
        json_data = json.loads(response.data)
        print(json_data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(
            json_data["error"], "Red_flag record already exists.")

    def test_04_user_create_red_flag_with_invalid_type(self):
        red_flag = {
            "comment": "We are facing this challenge",
            "_type": "i_dont_know",
            "images": "pic.jpg",
            "location": "Lat 1231 Long 1424",
            "videos": "vid.mp4"
        }
        response = self.client.post(
            "/api/v1/red_flags",
            headers=dict(
                Authorization='Bearer ' + GetToken.get_user_token()),
            json=red_flag)
        json_data = json.loads(response.data)
        self.assertEqual(400, response.status_code)
        self.assertEqual(json_data["error"], "given _type not allowed")

    def test_05_admin_create_red_flag(self):
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

    def test_06_admin_get_all_users_red_flags(self):
        response = self.client.get(
            "/api/v1/red_flags",
            headers=dict(
                Authorization='Bearer ' + GetToken.get_admin_token()))
        json_data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertIn("data", json_data)

    def test_07_user_get_users_red_flags(self):
        response = self.client.get(
            "/api/v1/red_flags",
            headers=dict(
                Authorization='Bearer ' + GetToken.get_user_token()))
        json_data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(200, response.status_code)
        self.assertIn("data", json_data)

    def test_08_get_user_red_flags_without_token(self):
        response = self.client.get("/api/v1/red_flags")
        json_data = json.loads(response.data)
        self.assertEqual(401, response.status_code)
        self.assertEqual(json_data["error"], "Invalid token")

    def test_09_get_user_red_flags(self):
        response = self.client.get(
            "/api/v1/red_flags",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()),
            json=self.red_flag)
        self.assertEqual(200, response.status_code)

    def test_10_get_user_single_red_flags_without_token(self):
        response = self.client.get("/api/v1/red_flags/1")
        json_data = json.loads(response.data)
        self.assertEqual(401, response.status_code)
        self.assertEqual(json_data["error"], "Invalid token")

    def test_11_get_user_single_red_flag(self):
        response = self.client.get(
            "/api/v1/red_flags/1",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()),
            json=self.red_flag)
        json_data = json.loads(response.data)
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            json_data["data"][0]["comment"], "We are facing this challenge")

    def test_12_edit_user_red_flag_location_without_token(self):
        location = {"location": "Kampala"}
        response = self.client.patch(
            "/api/v1/red_flags/1/location", json=location)
        json_data = json.loads(response.data)
        self.assertEqual(401, response.status_code)
        self.assertEqual(json_data["error"], "Invalid token")

    def test_13_edit_user_red_flag_location_with_wrong_URL(self):
        location = {"location": "Kampala"}
        response = self.client.patch(
            "/api/v1/red_flags/1/locat",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()),
            json=location)
        json_data = json.loads(response.data)
        self.assertEqual(404, response.status_code)
        self.assertEqual(
            json_data["error"],
            "Page Not found. Enter a valid URL"
        )

    def test_14_edit_user_red_flag_location(self):
        location = {"location": "Kampala"}
        response = self.client.patch(
            "/api/v1/red_flags/1/location",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()),
            json=location)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json_data["data"][0]["message"], "Updated red-flag location")

    def test_15_admin_edit_user_red_flag_location(self):
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

    def test_16_edit_user_red_flag_location_without_data(self):
        response = self.client.patch(
            "/api/v1/red_flags/1/location",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()))
        self.assertEqual(response.status_code, 400)
        json_data = json.loads(response.data)
        self.assertEqual(
            json_data["error"], "JSON request required")

    def test_17_edit_user_red_flag_comment_with_wrong_ID(self):
        comment = {"comment": "New comment"}
        response = self.client.patch(
            "/api/v1/red_flags/11/comment",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()),
            json=comment)
        self.assertEqual(response.status_code, 400)
        json_data = json.loads(response.data)
        self.assertEqual(
            json_data["error"], "Redflag record of id 11 doesn't exist")

    def test_18_edit_user_red_flag_comment_with_short_comment(self):
        comment = {"comment": "Today"}
        response = self.client.patch(
            "/api/v1/red_flags/1/comment",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()),
            json=comment)
        json_data = json.loads(response.data)
        self.assertEqual(
            json_data["error"],
            "comment must be atleast 10 to 40 characters")

    def test_19_admin_edit_user_red_flag_status(self):
        status = {"status": "resolved"}
        response = self.client.patch(
            "/api/v1/red_flags/1/status",
            headers=dict(Authorization='Bearer ' + GetToken.get_admin_token()),
            json=status)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json_data["data"][0]["message"], "Updated red-flag status")

    def test_20_admin_edit_user_red_flag_status_with_wrong_input(self):
        status = {"status": "draf"}
        response = self.client.patch(
            "/api/v1/red_flags/1/status",
            headers=dict(Authorization='Bearer ' + GetToken.get_admin_token()),
            json=status)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_data["error"], "given status not allowed")

    def test_21_admin_edit_user_red_flag_status_with_wrong_data_type(self):
        status = {"status": 34343}
        response = self.client.patch(
            "/api/v1/red_flags/1/status",
            headers=dict(Authorization='Bearer ' + GetToken.get_admin_token()),
            json=status)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_data["error"], "status must not be empty string")

    def test_22_user_edit_user_red_flag_status(self):
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

    def test_23_remove_user_red_flag_not_in_draft_state(self):
        response = self.client.delete(
            "/api/v1/red_flags/1",
            headers=dict(
                Authorization='Bearer ' +
                GetToken.get_user_token()))
        json_data = json.loads(response.data)
        print(json_data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json_data["error"],
            "Only redflag in draft state can be deleted"
        )

    def test_24_remove_user_red_flag_with_wrong_ID(self):
        response = self.client.delete(
            "/api/v1/red_flags/10",
            headers=dict(
                Authorization='Bearer ' +
                GetToken.get_user_token()))
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            json_data["error"],
            "Redflag record of id 10 doesn't exist"
        )

    def test_25_remove_user_red_flag(self):
        response = self.client.post(
            "/api/v1/red_flags",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()),
            json=self.red_flag)

        response = self.client.delete(
            "/api/v1/red_flags/2",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()))
        json_data = json.loads(response.data)
        print(json_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json_data["data"][0]["message"],
            "Red flag record has been deleted"
        )

    def test_26_admin_remove_user_red_flag(self):
        response = self.client.delete(
            "/api/v1/red_flags/1",
            headers=dict(
                Authorization='Bearer ' + GetToken.get_admin_token()))
        json_data = json.loads(response.data)
        self.assertEqual(403, response.status_code)
        self.assertEqual(
            json_data["error"],
            "Admin cannot access this resource")

    def test_27_method_not_allowed(self):
        response = self.client.patch("/api/v1/red_flags")
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            json_data["error"], "Method not allowed.")

    def test_28_admin_get_all_registered_users(self):
        response = self.client.get(
            "/api/v1/users",
            headers=dict(
                Authorization='Bearer ' + GetToken.get_admin_token()))
        self.assertEqual(200, response.status_code)

    def test_29_user_get_all_registered_users(self):
        response = self.client.get(
            "/api/v1/users",
            headers=dict(
                Authorization='Bearer ' + GetToken.get_user_token()))
        self.assertEqual(403, response.status_code)

    def test_30_user_create_red_flag_without_data(self):
        response = self.client.post(
            "/api/v1/red_flags",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()),
            json={})
        self.assertEqual(400, response.status_code)

    def test_31_user_create_red_flag_with_wrong_ID(self):
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

    def test_34_edit_user_red_flag_comment_not_in_draft(self):
        comment = {"comment": "My comment"}
        response = self.client.patch(
            "/api/v1/red_flags/1/comment",
            headers=dict(Authorization='Bearer ' + GetToken.get_user_token()),
            json=comment)
        json_data = json.loads(response.data)
        self.assertEqual(
            json_data["error"],
            "Only redflag in draft state can be edited")
