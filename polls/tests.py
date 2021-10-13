import datetime

from django.test import TestCase, Client

import json

test_username = "TEST_USER"
test_password = "TEST_PASSWORD"


class QuestionModelTests(TestCase):
    def test_polls_rest(self):
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

        r = do_request(
            "POST", "/users/", {"username": test_username, "password": test_password}
        )
        self.assertTrue(r.status_code == 200, "Could not create test user")

        r = do_request("POST", "/polls/")
        test_response(self, r, 400)

        r = do_request("POST", "/polls/", {"username": test_username})
        test_response(self, r, 400)
        r = do_request("POST", "/polls/", {"password": test_password})
        test_response(self, r, 400)
        r = do_request(
            "POST", "/polls/", {"username": test_username, "password": test_password}
        )
        test_response(self, r, 400)
        r = do_request(
            "POST",
            "/polls/",
            {"username": test_username, "password": test_password, "text": "What?"},
        )
        test_response(self, r, 400)
        r = do_request(
            "POST",
            "/polls/",
            {
                "username": "",
                "password": test_password,
                "text": "What?",
                "options": "IDK,LOL",
            },
        )
        test_response(self, r, 400)
        r = do_request(
            "POST",
            "/polls/",
            {
                "username": test_username,
                "password": "",
                "text": "What?",
                "options": "IDK,LOL",
            },
        )
        test_response(self, r, 400)
        r = do_request(
            "POST",
            "/polls/",
            {
                "username": test_username,
                "password": test_password,
                "text": "",
                "options": "IDK,LOL",
            },
        )
        test_response(self, r, 400)
        r = do_request(
            "POST",
            "/polls/",
            {
                "username": test_username,
                "password": test_password,
                "text": "What?",
                "options": "",
            },
        )
        test_response(self, r, 400)
        r = do_request(
            "POST",
            "/polls/",
            {
                "username": test_username,
                "password": test_password,
                "text": "What?",
                "options": "IDK,LOL",
            },
        )
        test_response(self, r, 200)

        r = do_request("GET", "/polls/")
        test_response(self, r, 200)
        self.assertTrue("questions" in r.json)
        found = False
        q = "0"
        for k in r.json["questions"]:
            try:
                int(k)
            except:
                self.assertTrue(False, '"questions" key is not int')

            if "What?" in r.json["questions"][k]:
                q = k
                found = True
                break

        self.assertTrue(found)

        r = do_request("GET", "/polls/", {"question": "100000"})
        test_response(self, r, 400)
        r = do_request("GET", "/polls/", {"question": int(q)})
        test_response(self, r, 200)
        self.assertTrue("user" in r.json)
        self.assertTrue(r.json["user"] == test_username)
        self.assertTrue("text" in r.json)
        self.assertTrue(r.json["text"] == "What?")
        self.assertTrue("publish date" in r.json)
        self.assertTrue("options" in r.json)
        found = 0
        for k in r.json["options"]:
            try:
                int(k)
            except:
                self.assertTrue(False, '"options" key is not int')

            self.assertTrue("text" in r.json["options"][k])
            self.assertTrue("votes" in r.json["options"][k])

            if r.json["options"][k]["text"] in ["IDK", "LOL"]:
                self.assertTrue(r.json["options"][k]["votes"] == 0)
                found += 1

        self.assertTrue(found == 2)

        r = do_request("PUT", "/polls/")
        test_response(self, r, 400)
        r = do_request("PUT", "/polls/", {"username": test_username})
        test_response(self, r, 400)
        r = do_request("PUT", "/polls/", {"password": test_password})
        test_response(self, r, 400)
        r = do_request(
            "PUT", "/polls/", {"username": test_username, "password": test_password}
        )
        test_response(self, r, 400)
        r = do_request(
            "PUT", "/polls/", {"username": "", "password": test_password, "question": q}
        )
        test_response(self, r, 400)
        r = do_request(
            "PUT", "/polls/", {"username": test_username, "password": "", "question": q}
        )
        test_response(self, r, 400)
        r = do_request(
            "PUT",
            "/polls/",
            {"username": test_username, "password": test_password, "question": 1000000},
        )
        test_response(self, r, 400)
        r = do_request(
            "PUT",
            "/polls/",
            {
                "username": test_username,
                "password": test_password,
                "question": q,
                "new-text": "My question?",
            },
        )
        test_response(self, r, 200)

        r = do_request("GET", "/polls/")
        found = False
        for k in r.json["questions"]:
            if r.json["questions"][k] == "My question?":
                found = True

        self.assertTrue(found)

        r = do_request(
            "PUT",
            "/polls/",
            {
                "username": test_username,
                "password": test_password,
                "question": q,
                "new-options": "32,LOL->WOW!,IDK->",
            },
        )
        test_response(self, r, 200)

        r = do_request("GET", "/polls/", {"question": q})
        found = 0
        for k in r.json["options"]:
            if r.json["options"][k]["text"] in ["WOW!", "32"]:
                found += 1

            elif r.json["options"][k]["text"] in ["IDK", "LOL"]:
                self.assertTrue(False)

        r = do_request("DELETE", "/polls/")
        test_response(self, r, 400)
        r = do_request("DELETE", "/polls/", {"username": test_username})
        test_response(self, r, 400)
        r = do_request("DELETE", "/polls/", {"password": test_password})
        test_response(self, r, 400)
        r = do_request(
            "DELETE", "/polls/", {"username": test_username, "password": test_password}
        )
        test_response(self, r, 400)
        r = do_request(
            "DELETE",
            "/polls/",
            {"username": "", "password": test_password, "question": q},
        )
        test_response(self, r, 400)
        r = do_request(
            "DELETE",
            "/polls/",
            {"username": test_username, "password": "", "question": q},
        )
        test_response(self, r, 400)
        r = do_request(
            "DELETE",
            "/polls/",
            {
                "username": test_username,
                "password": test_password,
                "question": 10000000,
            },
        )
        test_response(self, r, 400)
        r = do_request(
            "DELETE",
            "/polls/",
            {"username": test_username, "password": test_password, "question": q},
        )
        test_response(self, r, 200)

        r = do_request(
            "POST",
            "/polls/",
            {
                "username": test_username,
                "password": test_password,
                "text": "Sample?",
                "options": "a,b,c",
            },
        )
        r = do_request("GET", "/polls/")
        for k in r.json["questions"]:
            if r.json["questions"][k] == "Sample?":
                q = k
                break

        r = do_request("GET", "/polls/", {"question": q})
        o = 0
        for k in r.json["options"]:
            o = k
            break

        r = do_request("POST", "/polls/vote")
        test_response(self, r, 400)
        r = do_request("POST", "/polls/vote", {"username": test_username})
        test_response(self, r, 400)
        r = do_request("POST", "/polls/vote", {"password": test_password})
        test_response(self, r, 400)
        r = do_request(
            "POST",
            "/polls/vote",
            {"username": test_username, "password": test_password},
        )
        test_response(self, r, 400)
        r = do_request(
            "POST",
            "/polls/vote",
            {"username": test_username, "password": test_password},
        )
        test_response(self, r, 400)
        r = do_request(
            "POST",
            "/polls/vote",
            {"username": test_username, "password": test_password, "question": q},
        )
        test_response(self, r, 400)
        r = do_request(
            "POST",
            "/polls/vote",
            {"username": "", "password": test_password, "question": q, "options": o},
        )
        test_response(self, r, 400)
        r = do_request(
            "POST",
            "/polls/vote",
            {"username": test_username, "password": "", "question": q, "options": o},
        )
        test_response(self, r, 400)
        r = do_request(
            "POST",
            "/polls/vote",
            {
                "username": test_username,
                "password": test_password,
                "question": 10000000,
                "options": o,
            },
        )
        test_response(self, r, 400)
        r = do_request(
            "POST",
            "/polls/vote",
            {
                "username": test_username,
                "password": test_password,
                "question": q,
                "options": "10000",
            },
        )
        test_response(self, r, 400)
        r = do_request(
            "POST",
            "/polls/vote",
            {
                "username": test_username,
                "password": test_password,
                "question": q,
                "options": o,
            },
        )
        test_response(self, r, 200)

        r = do_request("GET", "/polls/", {"question": q})
        self.assertTrue(r.json["options"][o]["votes"] == 1)

        r = do_request("DELETE", "/polls/vote")
        test_response(self, r, 400)
        r = do_request("DELETE", "/polls/vote", {"username": test_username})
        test_response(self, r, 400)
        r = do_request("DELETE", "/polls/vote", {"password": test_password})
        test_response(self, r, 400)
        r = do_request(
            "DELETE",
            "/polls/vote",
            {"username": test_username, "password": test_password},
        )
        test_response(self, r, 400)
        r = do_request(
            "DELETE",
            "/polls/vote",
            {"username": "", "password": test_password, "question": q, "options": o},
        )
        test_response(self, r, 400)
        r = do_request(
            "DELETE",
            "/polls/vote",
            {"username": test_username, "password": "", "question": q, "options": o},
        )
        test_response(self, r, 400)
        r = do_request(
            "DELETE",
            "/polls/vote",
            {
                "username": test_username,
                "password": test_password,
                "question": 1000000,
                "options": o,
            },
        )
        test_response(self, r, 400)
        r = do_request(
            "DELETE",
            "/polls/vote",
            {
                "username": test_username,
                "password": test_password,
                "question": q,
                "options": "100000",
            },
        )
        test_response(self, r, 400)
        r = do_request(
            "DELETE",
            "/polls/vote",
            {
                "username": test_username,
                "password": test_password,
                "question": q,
                "options": o,
            },
        )
        test_response(self, r, 200)

        r = do_request("GET", "/polls/", {"question": q})
        self.assertTrue(r.json["options"][o]["votes"] == 0)

        r = do_request(
            "POST",
            "/polls/vote",
            {
                "username": test_username,
                "password": test_password,
                "question": q,
                "option": o,
            },
        )

        r = do_request(
            "DELETE",
            "/polls/vote",
            {"username": test_username, "password": test_password, "question": q},
        )
        test_response(self, r, 200)

        r = do_request("GET", "/polls/", {"question": q})
        self.assertTrue(r.json["options"][o]["votes"] == 0)
