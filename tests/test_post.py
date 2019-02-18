import unittest
import json
from main import app as tested_app
from db import db as tested_db
from config import TestConfig
from models.user import User
from models.post import Post
from models.like import Like

tested_app.config.from_object(TestConfig)


class TestUser(unittest.TestCase):
    def setUp(self):
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(User(id=1, name="Alice"))
        self.db.session.add(User(id=2, name="Bob"))
        self.db.session.add(Post(id=1, user_id=1, text="Post1"))
        self.db.session.add(Post(id=2, user_id=1, text="Post2"))
        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        self.db.drop_all()

    def test_get_all_post(self):
        response = self.app.get("/post/")
        self.assertEqual(response.status_code, 200)

        post_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(post_list), list)
        self.assertDictEqual(post_list[0], {"id": "1", "user_id": "1", "text": "Post1"})
        self.assertDictEqual(post_list[1], {"id": "2", "user_id": "1", "text": "Post2"})

    def test_get_post_with_valid_id(self):
        response = self.app.get("/post/1")
        self.assertEqual(response.status_code, 200)

        post = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(post, {"id": "1", "user_id": "1", "text": "Post1"})

    def test_get_post_with_invalid_id(self):
        response = self.app.get("/post/1000000")
        self.assertEqual(response.status_code, 404)

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 404, "msg": "Not Found"})

    def test_get_post_likes(self):
        self.db.session.add(Like(id=1, user_id=1, post_id="1"))
        self.db.session.add(Like(id=2, user_id=2, post_id="1"))

        response = self.app.get("/post/1/likes")
        self.assertEqual(response.status_code, 200)

        like_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(like_list), list)
        self.assertDictEqual(like_list[0], {"id": "1", "user_id": "1", "post_id": "1"})

    def test_put_post(self):
        initial_count = Post.query.count()

        response = self.app.put("/post/", data={"user_id": "1", "text": "Post3"})
        self.assertEqual(response.status_code, 200)

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"id": "3", "user_id": "1", "text": "Post3"})

        updated_count = Post.query.count()
        self.assertEqual(updated_count, initial_count+1)

    def test_put_post_missing_text(self):
        response = self.app.put("/post/", data={"user_id": "1"})

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 403, "msg": "Missing 'text'"})

    def test_put_post_missing_user_id(self):
        response = self.app.put("/post/", data={"text": "Post"})

        body = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(body, {"code": 403, "msg": "Missing 'user_id'"})
