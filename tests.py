import json
import unittest
from unittest import TestCase

from source.db import db, SiteUser, Book
from main import create_app

app = create_app('TEST')


class TestUser(TestCase):
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

    def test_01_get_empty_table(self):
        resp = app.test_client().get('/users')
        self.assertEqual(200, resp.status_code)
        self.assertEqual([], resp.json)

    def test_02_get_user(self):
        example_user = SiteUser(username='vasyl', group='user')
        db.session.add(example_user)
        db.session.commit()

        resp = app.test_client().get('/users')
        expected = [{"id": 1, "username": "vasyl", "group": "user", "address": {}, "library": [], "wishlist": []}]
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)

        resp = app.test_client().get('/users/1')
        expected = {"id": 1, "username": "vasyl", "group": "user", "address": {}, "library": [], "wishlist": []}
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)

    def test_03_get_wrong_user(self):
        resp = app.test_client().get('/users/23')
        self.assertEqual(404, resp.status_code)
        self.assertEqual('No such user', resp.json['ErrorMessage'])

    def test_04_user_post(self):
        data = json.dumps({'username': 'petro', 'group': 'admin'})
        resp = app.test_client().post('/users', data=data, content_type='application/json')
        expected = [
            {"id": 1, "username": "vasyl", "group": "user", "address": {}, "library": [], "wishlist": []},
            {"id": 2, "username": "petro", "group": "admin", "address": {}, "library": [], "wishlist": []}
        ]
        self.assertEqual(201, resp.status_code)
        self.assertEqual(expected, resp.json)

    def test_05_user_post_not_enough(self):
        data = json.dumps({'username': 'joker'})
        resp = app.test_client().post('/users', data=data, content_type='application/json')
        self.assertEqual(400, resp.status_code)
        self.assertEqual('Not enough arguments', resp.json['ErrorMessage'])

    def test_06_user_post_existing_name(self):
        data = json.dumps({'username': 'petro', 'group': 'admin'})
        resp = app.test_client().post('/users', data=data, content_type='application/json')
        self.assertEqual(409, resp.status_code)
        self.assertEqual('This username already exists', resp.json['ErrorMessage'])

    def test_07_user_patch(self):
        data = json.dumps({'username': 'killer99', 'group': 'user'})
        resp = app.test_client().patch('/users/2', data=data, content_type='application/json')
        expected = [
            {"id": 1, "username": "vasyl", "group": "user", "address": {}, "library": [], "wishlist": []},
            {"id": 2, "username": "killer99", "group": "user", "address": {}, "library": [], "wishlist": []}
        ]
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)

        # check if it will work the second time (it must!)
        resp = app.test_client().patch('/users/2', data=data, content_type='application/json')
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)

    def test_08_user_patch_wrong_id(self):
        data = json.dumps({'username': 'killer99', 'group': 'user'})
        resp = app.test_client().patch('/users/3', data=data, content_type='application/json')
        self.assertEqual(404, resp.status_code)
        self.assertEqual('No such user', resp.json['ErrorMessage'])

    def test_09_user_delete(self):
        resp = app.test_client().delete('/users/2')
        expected = [{"id": 1, "username": "vasyl", "group": "user", "address": {}, "library": [], "wishlist": []}]
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)

    def test_10_delete_wrong_user(self):
        resp = app.test_client().delete('/users/3')
        self.assertEqual(404, resp.status_code)
        self.assertEqual('No such user', resp.json['ErrorMessage'])


class TestBook(TestCase):
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

    def test_11_get_empty(self):
        resp = app.test_client().get('/books')
        self.assertEqual(200, resp.status_code)
        self.assertEqual([], resp.json)

    def test_12_get_books(self):
        example_book = Book(isbn='978-1593279288',
                                name='Python Crash Course, 2nd Edition: A Hands-On'
                                     ', Project-Based Introduction to Programming',
                                author='Eric Matthes')
        db.session.add(example_book)
        db.session.commit()

        resp = app.test_client().get('/books')
        expected = [{"id": 1, "name": "Python Crash Course, 2nd Edition: A Hands-On, "
                                      "Project-Based Introduction to Programming",
                     "author": "Eric Matthes", "translator": None, "genre": None, "year": None, "publisher": None,
                     "isbn": "978-1593279288"}]
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)

        resp = app.test_client().get('/books/1')
        expected = {"id": 1, "name": "Python Crash Course, 2nd Edition: A Hands-On, "
                                     "Project-Based Introduction to Programming",
                    "author": "Eric Matthes", "translator": None, "genre": None, "year": None, "publisher": None,
                    "isbn": "978-1593279288"}
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)

    def test_13_get_wrong_book(self):
        resp = app.test_client().get('/books/3')
        self.assertEqual(404, resp.status_code)
        self.assertEqual('No such book', resp.json['ErrorMessage'])

    def test_14_post_book(self):
        data = json.dumps({'name': 'The outsider', 'author': 'Stephen King'})
        resp = app.test_client().post('/books', data=data, content_type='application/json')
        expected = [
                    {
                        "id": 1, "name": "Python Crash Course, 2nd Edition: A Hands-On, "
                                         "Project-Based Introduction to Programming",
                        "author": "Eric Matthes", "translator": None, "genre": None, "year": None, "publisher": None,
                        "isbn": "978-1593279288"},
                    {
                        "id": 2, "name": "The outsider", "author": "Stephen King", "translator": None, "genre": None,
                        "year": None, "publisher": None, "isbn": None
                    }
                    ]
        self.assertEqual(201, resp.status_code)
        self.assertEqual(expected, resp.json)

    def test_15_post_books_not_enough(self):
        data = json.dumps({'name': 'Game of Thrones'})
        resp = app.test_client().post('/books', data=data, content_type='application/json')
        self.assertEqual(400, resp.status_code)
        self.assertEqual('Not enough arguments', resp.json['ErrorMessage'])

    def test_16_post_excessive_info(self):
        data = json.dumps({'name': 'Game of Thrones', 'author': 'George R. R. Martin', 'color': 'black'})
        resp = app.test_client().post('/books', data=data, content_type='application/json')
        self.assertEqual(400, resp.status_code)
        self.assertEqual('Excessive arguments posted', resp.json['ErrorMessage'])

if __name__ == '__main__':
    unittest.main()
