from app.routes import app
import unittest
import json


class TestApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client(self)

    def test_home(self):
        response = self.client.get("/")
        self.assertEqual(200, response.status_code)
        self.assertIn("Welcome to api", str(response.data))

    def test_create_red_flag(self):
        red_flag = {"type": "red-flag", "createdBy": 1234,
                    "location": "Masaka", "status": "resolved",
                    "images": "pic1.jpg", "videos": "vid.mp4",
                    "comment": "comment one"}
        response = self.client.post("/api/v1/red_flags", json=red_flag)
        json_data = json.loads(response.data)
        self.assertTrue(response.is_json, True)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            json_data["data"][0]["message"],
            "Created red-flag record")


    def test_for_red_flag_data_types_and_missing_data(self):
        red_flag = {"type": "red-flag", "createdBy": "Fred",
                    "status": "resolved", "images": "pic1.jpg",
                     "videos": "vid.mp4","comment": "comment one",
                      "location": "Masaka"}
        response = self.client.post("api/v1/red_flags", json=red_flag)
        json_data = json.loads(response.data)
        self.assertEqual(json_data["error"], "createdBy must be an int")

        red_flag = {"type": "red-flag", "createdBy": 12345,
                    "status": 2345, "images": "pic1.jpg", "videos": "vid.mp4",
                    "comment": "comment one", "location": "Masaka"}
        response = self.client.post("api/v1/red_flags", json=red_flag)
        json_data = json.loads(response.data)
        self.assertEqual(json_data["error"], "status must not be empty string")

        red_flag = {
            "type": "red-flag","createdBy": 1234,"status": "resolved",
            "images": "pic1.jpg","videos": "vid.mp4","comment": "comment one",
            "location": 1234
            }
        response = self.client.post("api/v1/red_flags", json=red_flag)
        json_data = json.loads(response.data)
        self.assertEqual(
            json_data["error"],"location must not be empty string")

        red_flag = {
            "type": "","createdBy": 1234,"status": "resolved",
            "images": "pic1.jpg","videos": "vid.mp4","comment": " ",
            "location": "Masaka"
            }
        response = self.client.post("api/v1/red_flags", json=red_flag)
        json_data = json.loads(response.data)
        self.assertEqual(
            json_data["error"],
            "comment must not be empty string")

    def test_create_red_flag_without_data(self):
        response = self.client.post("/api/v1/red_flags")
        self.assertEqual(response.status_code, 400)
        json_data = json.loads(response.data)
        self.assertEqual(
            json_data["error"],"JSON request required")

    def test_get_all_red_flags(self):
        response = self.client.get("/api/v1/red_flags")
        self.assertTrue(response.is_json, True)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_data["data"][0]["status"], "resolved")

    def test_get_all_redflags_with_wrong_url(self):
        response = self.client.get("/api/v1/red_flags/")
        self.assertEqual(response.status_code, 404)

    def test_get_single_red_flag(self):
        response = self.client.get("/api/v1/red_flags/1")
        self.assertTrue(response.is_json, True)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("data", json_data)

    def test_get_single_redflag_with_wrong_url(self):
        response = self.client.get("/api/v1/red_flags/10//")
        self.assertEqual(response.status_code, 404)

    def test_get_single_redflag_with_wrong_ID(self):
        response = self.client.get("/api/v1/red_flags/10")
        self.assertEqual(response.status_code, 400)

    def test_edit_red_flag_location(self):
        location = {"location": "Kampala"}
        response = self.client.patch(
            "/api/v1/red_flags/1/location", json=location)
        self.assertEqual(response.status_code, 200)

    def test_edit_red_flag_location_wrong_data_type(self):
        location = {"location": 1233}
        response = self.client.patch(
            "/api/v1/red_flags/1/location", json=location)
        self.assertEqual(response.status_code, 400)

    def test_edit_red_flag_location_without_data(self):
        response = self.client.patch("/api/v1/red_flags/1/location")
        self.assertEqual(response.status_code, 400)
        json_data = json.loads(response.data)
        self.assertEqual(
            json_data["error"],"JSON request required")

    def test_edit_red_flag_location_with_wrong_url(self):
        response = self.client.patch("/api/v1/red_flags/1/location///")
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_data["error"],"Page Not found. Enter a valid URL")

    def test_edit_red_flag_location_with_wrong_ID(self):
        response = self.client.patch("/api/v1/red_flags/10/location")
        self.assertEqual(response.status_code, 400)

    def test_edit_red_flag_comment(self):
        comment = {"comment": "New comment"}
        response = self.client.patch(
            "/api/v1/red_flags/1/comment", json=comment)
        self.assertTrue(response.is_json, True)
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json_data["data"][0]["message"],
            "Updated red-flag comment")
    

    def test_edit_red_flag_comment_without_json(self):
        response = self.client.patch("/api/v1/red_flags/1/comment")
        self.assertEqual(response.status_code, 400)
        json_data = json.loads(response.data)
        self.assertEqual(
            json_data["error"],"JSON request required")

    def test_edit_red_flag_comment_wrong_data_type(self):
        comment = {"comment": 1233}
        response = self.client.patch(
            "/api/v1/red_flags/1/comment", json=comment)
        json_data = json.loads(response.data)
        self.assertEqual(
            json_data["error"],
            "comment must not be empty string")

    def test_edit_red_flag_comment_wrong_url(self):
        response = self.client.patch("/api/v1/red_flags/1/comment//")
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_data["error"],"Page Not found. Enter a valid URL")

    def test_edit_red_flag_comment_with_wrong_ID(self):
        response = self.client.patch("/api/v1/red_flags/10/comment")
        self.assertEqual(response.status_code, 400)

    def test_remove_red_flag(self):
        response = self.client.delete("/api/v1/red_flags/1")
        self.assertTrue(response.is_json, True)
        json_data = json.loads(response.data)
        print("returned data", json_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            json_data["data"][0]["message"],
            "Red flag record has been deleted")

    def test_remove_red_flag_with_wrong_data(self):
        response = self.client.delete("/api/v1/red_flags/10")
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_data["error"],"ID Not found. Enter a valid ID")

    def test_remove_red_flag_with_wrong_url(self):
        response = self.client.delete("/api/v1/red_flags/10//")
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(json_data["error"],"Page Not found. Enter a valid URL")

    def test_remove_red_flag_with_wrong_ID(self):
        response = self.client.delete("/api/v1/red_flags/10")
        self.assertEqual(response.status_code, 400)
    
    def test_method_not_allowed(self):
        response = self.client.delete("/api/v1/red_flags")
        json_data = json.loads(response.data)
        self.assertEqual(response.status_code, 405)
        self.assertEqual(
            json_data["error"],"Method not allowed. Check your HTTP METHOD")

