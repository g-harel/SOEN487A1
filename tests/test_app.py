import unittest
import json
from main import app as tested_app
from config import TestConfig

tested_app.config.from_object(TestConfig)


class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = tested_app.test_client()

    def test_404_on_invalid_url(self):
        response = self.app.get("/something")
        self.assertEqual(response.status_code, 404)

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Not Found"})

    def test_root(self):
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)

        body = json.loads(str(response.data, "utf8"))
        self.assertEqual(body["title"], "SOEN487 Assignment 1")
        student = body["student"]
        self.assertEqual(student["id"], "40006459")
        self.assertEqual(student["name"], "Gabriel Harel")
