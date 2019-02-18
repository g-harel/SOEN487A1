import unittest
import json
from main import app as tested_app
from db import db as tested_db
from config import TestConfig
from models.user import User
from models.post import Post
from models.like import Like

tested_app.config.from_object(TestConfig)


class TestLike(unittest.TestCase):
    def setUp(self):
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(User(id=1, name="Alice"))
        self.db.session.add(User(id=2, name="Bob"))
        self.db.session.add(Post(id=1, user_id=1, text="Post1"))
        self.db.session.add(Post(id=2, user_id=1, text="Post2"))
        self.db.session.add(Like(id=1, user_id=2, post_id=1))
        self.db.session.add(Like(id=2, user_id=2, post_id=2))
        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        self.db.drop_all()

    def test_get_all_like(self):
        response = self.app.get("/like/")
        self.assertEqual(response.status_code, 200)

        like_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(like_list), list)
        self.assertDictEqual(like_list[0], {"id": "1", "user_id": "2", "post_id": "1"})
        self.assertDictEqual(like_list[1], {"id": "2", "user_id": "2", "post_id": "2"})

    def test_get_like_with_valid_id(self):
        response = self.app.get("/like/1")
        self.assertEqual(response.status_code, 200)

        like = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(like, {"id": "1", "user_id": "2", "post_id": "1"})

    def test_get_like_with_invalid_id(self):
        response = self.app.get("/like/1000000")
        self.assertEqual(response.status_code, 404)

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Not Found"})

    def test_put_like(self):
        initial_count = Like.query.count()

        response = self.app.put("/like/", data={"user_id": "1", "post_id": "1"})
        self.assertEqual(response.status_code, 200)

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"id": "3", "user_id": "1", "post_id": "1"})

        updated_count = Like.query.count()
        self.assertEqual(updated_count, initial_count+1)

    def test_put_like_duplicate(self):
        response = self.app.put("/like/", data={"user_id": "1", "post_id": "1"})
        self.assertEqual(response.status_code, 200)

        response = self.app.put("/like/", data={"user_id": "1", "post_id": "1"})
        self.assertEqual(response.status_code, 500)
