import json
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

    def test_user_post(self):
        data = json.dumps({'username': 'petro', 'group': 'admin'})
        resp = app.test_client().post('/users', data=data, content_type='application/json')
        expected = [
                    {"id": 1, "username": "vasyl", "group": "user", "address": {}, "library": [], "wishlist": []},
                    {"id": 2, "username": "petro", "group": "admin", "address": {}, "library": [], "wishlist": []}
                    ]
        self.assertEqual(201, resp.status_code)
        self.assertEqual(expected, resp.json)

    def test_user_post_not_enough(self):
        data = json.dumps({'username': 'joker'})
        resp = app.test_client().post('/users', data=data, content_type='application/json')
        self.assertEqual(400, resp.status_code)
        self.assertEqual('Not enough arguments', resp.json['ErrorMessage'])

    def test_user_post_existing_name(self):
        data = json.dumps({'username': 'petro', 'group': 'admin'})
        resp = app.test_client().post('/users', data=data, content_type='application/json')
        self.assertEqual(409, resp.status_code)
        self.assertEqual('This username already exists', resp.json['ErrorMessage'])

if __name__ == '__main__':
    unittest.main()
