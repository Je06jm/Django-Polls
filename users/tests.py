from typing import Tuple
from django import test
from django.http import request
from django.test import TestCase, Client
from requests.sessions import Request

from .models import *
from .views import *
import requests, json

test_username = "_TEST_USER_"
test_password = "_TEST_PASSWORD_1234_"

# Create your tests here.
class UserCRUDTest(TestCase):
    def test_user_rest(self):
        c = Client()

        def do_request(method, path, header_data={}):
            data = {}
            for header in header_data:
                data.update({"HTTP_" + header: header_data[header]})
            r = c.generic(method, path, content_type="application/json", **data)
            try:
                r.json = json.loads(r.content.decode())

            except:
                pass

            return r

        def test_response(self, response, expected_status, expected_message=None):
            self.assertTrue(r.status_code == expected_status)
            if expected_message:
                self.assertTrue("message" in response)
                self.assertTrue(response["message"] == expected_message)

        r = do_request("POST", "/users/")
        test_response(self, r, 400)
        r = do_request("POST", "/users/", {"username": test_username})
        test_response(self, r, 400)
        r = do_request("POST", "/users/", {"password": test_password})
        test_response(self, r, 400)
        r = do_request("POST", "/users/", {"username": test_username, "password": ""})
        test_response(self, r, 400)
        r = do_request("POST", "/users/", {"username": "", "password": test_password})
        test_response(self, r, 400)
        r = do_request(
            "POST", "/users/", {"username": test_username, "password": test_password}
        )
        test_response(self, r, 200)

        r = do_request("GET", "/users/")
        test_response(self, r, 200)
        self.assertTrue("users" in r.json)
        self.assertTrue(test_username in r.json["users"])

        r = do_request("GET", "/users/", {"username": "_RANDOM_"})
        test_response(self, r, 400)
        r = do_request("GET", "/users/", {"username": test_username})
        test_response(self, r, 200)
        self.assertTrue("date_joined" in r.json)
        self.assertTrue("is_staff" in r.json)
        self.assertFalse(r.json["is_staff"])

        r = do_request("PUT", "/users/")
        test_response(self, r, 400)
        r = do_request("PUT", "/users/", {"username": test_username})
        test_response(self, r, 400)
        r = do_request("PUT", "/users/", {"password": test_password})
        test_response(self, r, 400)
        r = do_request(
            "PUT", "/users/", {"username": test_username, "password": test_password}
        )
        test_response(self, r, 400)
        r = do_request(
            "PUT",
            "/users/",
            {
                "username": "",
                "password": test_password,
                "new-password": test_password + "01",
            },
        )
        test_response(self, r, 400)
        r = do_request(
            "PUT",
            "/users/",
            {
                "username": test_username,
                "password": "",
                "new-password": test_password + "01",
            },
        )
        test_response(self, r, 400)
        r = do_request(
            "PUT",
            "/users/",
            {"username": "", "password": "", "new-password": test_password + "01"},
        )
        test_response(self, r, 400)
        r = do_request(
            "PUT",
            "/users/",
            {"username": test_username, "password": test_password, "new-password": ""},
        )
        test_response(self, r, 400)
        r = do_request(
            "PUT",
            "/users/",
            {"username": "", "password": test_password, "new-password": ""},
        )
        test_response(self, r, 400)
        r = do_request(
            "PUT",
            "/users/",
            {"username": test_username, "password": "", "new-password": ""},
        )
        test_response(self, r, 400)
        r = do_request(
            "PUT", "/users/", {"username": "", "password": "", "new-password": ""}
        )
        test_response(self, r, 400)
        r = do_request(
            "PUT",
            "/users/",
            {
                "username": test_username,
                "password": test_password,
                "new-password": test_password + "01",
            },
        )
        test_response(self, r, 200)
        r = do_request(
            "PUT",
            "/users/",
            {
                "username": test_username,
                "password": test_password + "01",
                "new-password": test_password,
            },
        )

        r = do_request("DELETE", "/users/")
        test_response(self, r, 400)
        r = do_request("DELETE", "/users/", {"username": test_username})
        test_response(self, r, 400)
        r = do_request("DELETE", "/users/", {"password": test_password})
        test_response(self, r, 400)
        r = do_request("DELETE", "/users/", {"username": "", "password": test_password})
        test_response(self, r, 400)
        r = do_request("DELETE", "/users/", {"username": test_username, "password": ""})
        test_response(self, r, 400)
        r = do_request(
            "DELETE", "/users/", {"username": test_username, "password": test_password}
        )
        test_response(self, r, 200)
