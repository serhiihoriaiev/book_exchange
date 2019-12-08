import unittest
from unittest import TestCase

from source.db import db, SiteUser
from main import create_app

app = create_app('TEST')


class TestBooksExchange(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app_context = app.app_context()
        cls.app_context.push()
        db.create_all()

    @classmethod
    def tearDownClass(cls):
        db.session.remove()
        db.drop_all()
        cls.app_context.pop()

    def test_get_empty_table(self):
        resp = app.test_client().get('/users')
        self.assertEqual(200, resp.status_code)
        self.assertEqual([], resp.json)

    def test_get_user(self):
        example_user = SiteUser(username='vasyl', group='user')
        db.session.add(example_user)
        db.session.commit()

        resp = app.test_client().get('/users')
        expected = [{"id": 1, "username": "vasyl", "group": "user", "address": {}, "library": [], "wishlist": []}]
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)


if __name__ == '__main__':
    unittest.main()
