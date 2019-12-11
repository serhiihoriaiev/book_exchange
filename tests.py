import json
import unittest
from unittest import TestCase

from source.db import db, SiteUser, Book, Address
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
        expected = {"id": 2, "username": "killer99", "group": "user", "address": {}, "library": [], "wishlist": []}
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

    def test_11_get_empty_addresses(self):
        resp = app.test_client().get('/addr')
        self.assertEqual(200, resp.status_code)
        self.assertEqual([], resp.json)

    def test_12_get_all_addresses(self):
        data = Address(street_addr='Krylova str, 96', city='Los Angeles', region='CA', zip='12345-6789',
                       country='USA')
        db.session.add(data)
        db.session.commit()

        resp = app.test_client().get('/addr')
        expected = [{'id': 1, 'street_addr': 'Krylova str, 96', 'city': 'Los Angeles',
                     'region': 'CA', 'zip': '12345-6789', 'country': 'USA'}]
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)

    def test_13_get_address_by_id(self):
        resp = app.test_client().get('/addr/1')
        expected = {'id': 1, 'street_addr': 'Krylova str, 96', 'city': 'Los Angeles',
                    'region': 'CA', 'zip': '12345-6789', 'country': 'USA'}
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)

    def test_14_post_new_address(self):
        data = json.dumps({'street_addr': 'Bandera pr., 22, app.4', 'city': 'Kyiv',
                           'region': 'Kyivska oblast', 'zip': '40321', 'country': 'Ukraine'})
        app.test_client().post('/addr', data=data, content_type='application/json')

        data = json.dumps({'street_addr': 'Lomonosov str, 28', 'city': 'Kharkiv',
                           'region': 'Kharkivska oblast', 'zip': '61020', 'country': 'Ukraine'})
        resp = app.test_client().post('/addr', data=data, content_type='application/json')

        expected = [
            {'id': 1, 'street_addr': 'Krylova str, 96', 'city': 'Los Angeles',
             'region': 'CA', 'zip': '12345-6789', 'country': 'USA'},
            {'id': 2, 'street_addr': 'Bandera pr., 22, app.4', 'city': 'Kyiv',
             'region': 'Kyivska oblast', 'zip': '40321', 'country': 'Ukraine'},
            {'id': 3, 'street_addr': 'Lomonosov str, 28', 'city': 'Kharkiv',
             'region': 'Kharkivska oblast', 'zip': '61020', 'country': 'Ukraine'}
        ]
        self.assertEqual(201, resp.status_code)
        self.assertEqual(expected, resp.json)


    def test_15_post_not_enough_data(self):
        data = json.dumps({'street_addr': 'Stalevarov str, 20'})
        resp = app.test_client().post('/addr', data=data, content_type='application/json')
        self.assertEqual(400, resp.status_code)
        self.assertEqual('Not enough arguments', resp.json['ErrorMessage'])

    def test_16_patch_addr_info(self):
        data = json.dumps({'street_addr': 'Stalevarov str, 20'})
        resp = app.test_client().patch('/addr/1', data=data, content_type='application/json')
        expected = {'id': 1, 'street_addr': 'Stalevarov str, 20', 'city': 'Los Angeles',
                    'region': 'CA', 'zip': '12345-6789', 'country': 'USA'}
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)

    def test_17_patch_addr_id(self):
        data = json.dumps({'id': 4, 'street_addr': 'Stalevarov str, 20'})
        resp = app.test_client().patch('/addr/1', data=data, content_type='application/json')
        self.assertEqual(403, resp.status_code)
        self.assertEqual('You can''t change ID', resp.json['ErrorMessage'])

    def test_18_patch_address_not_exist(self):
        data = json.dumps({'street_addr': 'Stalevarov str, 20'})
        resp = app.test_client().patch('/addr/5', data=data, content_type='application/json')
        self.assertEqual(404, resp.status_code)
        self.assertEqual('No such address', resp.json['ErrorMessage'])

    def test_19_delete_address(self):
        resp = app.test_client().delete('/addr/2')
        expected = [{'id': 1, 'street_addr': 'Stalevarov str, 20', 'city': 'Los Angeles',
                     'region': 'CA', 'zip': '12345-6789', 'country': 'USA'},
                    {'id': 3, 'street_addr': 'Lomonosov str, 28', 'city': 'Kharkiv',
                     'region': 'Kharkivska oblast', 'zip': '61020', 'country': 'Ukraine'}]
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)

    def test_20_delete_not_existent_addr(self):
        resp = app.test_client().delete('/addr/6')
        self.assertEqual(404, resp.status_code)
        self.assertEqual('No such address', resp.json['ErrorMessage'])

    def test_21_delete_addr_not_specified(self):
        resp = app.test_client().delete('/addr')
        self.assertEqual(400, resp.status_code)
        self.assertEqual('Address not specified', resp.json['ErrorMessage'])

    def test_22_post_existing_address(self):
        data = json.dumps({'street_addr': 'Stalevarov str, 20', 'city': 'Los Angeles',
                           'region': 'CA', 'zip': '12345-6789', 'country': 'USA'})
        resp = app.test_client().post('/addr', data=data, content_type='application/json')
        self.assertEqual(403, resp.status_code)
        self.assertEqual('This address already exists', resp.json['ErrorMessage'])

    def test_23_add_address_to_user(self):
        data = json.dumps({'address_id': 1})
        resp = app.test_client().patch('/users/1', data=data, content_type='application/json')
        expected = {
                    "id": 1, "username": "vasyl", "group": "user",
                    "address": {
                        'id': 1, 'street_addr': 'Stalevarov str, 20', 'city': 'Los Angeles',
                        'region': 'CA', 'zip': '12345-6789', 'country': 'USA'
                    }, "library": [], "wishlist": []
                    }
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)

    def test_24_change_user_address(self):
        data = json.dumps({'address_id': 3})
        resp = app.test_client().patch('/users/1', data=data, content_type='application/json')
        expected = {
            "id": 1, "username": "vasyl", "group": "user",
            "address": {
                'id': 3, 'street_addr': 'Lomonosov str, 28', 'city': 'Kharkiv',
                'region': 'Kharkivska oblast', 'zip': '61020', 'country': 'Ukraine'
            }, "library": [], "wishlist": []
        }
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)

    def test_25_add_wrong_address_to_user(self):
        data = json.dumps({'address_id': 5})
        resp = app.test_client().patch('/users/1', data=data, content_type='application/json')
        self.assertEqual(404, resp.status_code)
        self.assertEqual('No such address', resp.json['ErrorMessage'])

    def test_26_add_address_to_wrong_user(self):
        data = json.dumps({'address_id': 1})
        resp = app.test_client().patch('/users/24', data=data, content_type='application/json')
        self.assertEqual(404, resp.status_code)
        self.assertEqual('No such user', resp.json['ErrorMessage'])

    def test_27_delete_address_from_user(self):
        data = json.dumps({'address_id': None})
        resp = app.test_client().patch('/users/1', data=data, content_type='application/json')
        expected = {
            "id": 1, "username": "vasyl", "group": "user",
            "address": {}, "library": [], "wishlist": []
        }
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)


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

    def test_01_get_empty(self):
        resp = app.test_client().get('/books')
        self.assertEqual(200, resp.status_code)
        self.assertEqual([], resp.json)

    def test_02_get_books(self):
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

    def test_03_get_wrong_book(self):
        resp = app.test_client().get('/books/3')
        self.assertEqual(404, resp.status_code)
        self.assertEqual('No such book', resp.json['ErrorMessage'])

    def test_04_post_book(self):
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

    def test_05_post_books_not_enough(self):
        data = json.dumps({'name': 'Game of Thrones'})
        resp = app.test_client().post('/books', data=data, content_type='application/json')
        self.assertEqual(400, resp.status_code)
        self.assertEqual('Not enough arguments', resp.json['ErrorMessage'])

    def test_06_post_excessive_info(self):
        data = json.dumps({'name': 'Game of Thrones', 'author': 'George R. R. Martin', 'color': 'black'})
        resp = app.test_client().post('/books', data=data, content_type='application/json')
        self.assertEqual(400, resp.status_code)
        self.assertEqual('Excessive arguments posted', resp.json['ErrorMessage'])

    def test_07_patch_book(self):
        data = json.dumps({'genre': 'programming', 'year': 2019})
        resp = app.test_client().patch('/books/1', data=data, content_type='application/json')
        expected = {
            "id": 1, "name": "Python Crash Course, 2nd Edition: A Hands-On, "
                             "Project-Based Introduction to Programming",
            "author": "Eric Matthes", "translator": None, "genre": "programming", "year": 2019,
            "publisher": None, "isbn": "978-1593279288"
        }
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)

        # check if it will work the second time (it must!)
        resp = app.test_client().patch('/books/1', data=data, content_type='application/json')
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)

    def test_08_patch_book_not_specified(self):
        data = json.dumps({'genre': 'programming', 'year': 2019})
        resp = app.test_client().patch('/books', data=data, content_type='application/json')
        self.assertEqual(400, resp.status_code)
        self.assertEqual('Book not specified', resp.json['ErrorMessage'])

    def test_09_delete_book(self):
        resp = app.test_client().delete('/books/1')
        expected = [{
            "id": 2, "name": "The outsider", "author": "Stephen King", "translator": None, "genre": None,
            "year": None, "publisher": None, "isbn": None
        }]
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)

    def test_10_delete_wrong_book(self):
        resp = app.test_client().delete('/books/5')
        self.assertEqual(404, resp.status_code)
        self.assertEqual('No such book', resp.json['ErrorMessage'])

    def test_11_delete_wrong_query(self):
        resp = app.test_client().delete('/books')
        self.assertEqual(400, resp.status_code)
        self.assertEqual('Book not specified', resp.json['ErrorMessage'])


if __name__ == '__main__':
    unittest.main()
