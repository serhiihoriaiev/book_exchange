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
        expected = [{"id": 1, "username": "vasyl", "group": "user", "address": {}}]
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)

        resp = app.test_client().get('/users/1')
        expected = {"id": 1, "username": "vasyl", "group": "user", "address": {}}
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
            {"id": 1, "username": "vasyl", "group": "user", "address": {}},
            {"id": 2, "username": "petro", "group": "admin", "address": {}}
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
        expected = {"id": 2, "username": "killer99", "group": "user", "address": {}}
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
        expected = [{"id": 1, "username": "vasyl", "group": "user", "address": {}}]
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
                    }
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
            }
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
            "address": {}
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


class LibraryTesting(TestCase):
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

    def test_01_get_empty_library(self):
        data = json.dumps({'username': 'petro', 'group': 'admin'})
        app.test_client().post('/users', data=data, content_type='application/json')

        resp = app.test_client().get('/users/1/library')
        expected = {'books': [], 'hidden_lib': False, 'id': 1}
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)

    def test_02_add_book_to_lib(self):
        example_book = Book(isbn='978-1593279288',
                            name='Python Crash Course, 2nd Edition: A Hands-On'
                                 ', Project-Based Introduction to Programming',
                            author='Eric Matthes')
        db.session.add(example_book)
        db.session.commit()

        data = json.dumps({'book_id': 1})
        resp = app.test_client().post('/users/1/library', data=data, content_type='application/json')
        expected = {'books': [{"book": {"id": 1, "name": "Python Crash Course, 2nd Edition: A Hands-On, "
                                        "Project-Based Introduction to Programming",
                                        "author": "Eric Matthes", "translator": None, "genre": None, "year": None,
                                        "publisher": None, "isbn": "978-1593279288"},
                              "hidden": False, "status": "Available for exchange"}],
                    'hidden_lib': False, 'id': 1}
        self.assertEqual(201, resp.status_code)
        self.assertEqual(expected, resp.json)

    def test_03_add_more_books_to_lib(self):
        example_book = Book(isbn='978-0132350884',
                            name='Clean Code: A Handbook of Agile Software Craftsmanship',
                            author='Robert C. Martin')
        db.session.add(example_book)
        db.session.commit()

        data = json.dumps({'book_id': 2})
        resp = app.test_client().post('/users/1/library', data=data, content_type='application/json')
        expected = {'books': [{"book": {"id": 1, "name": "Python Crash Course, 2nd Edition: A Hands-On, "
                                                         "Project-Based Introduction to Programming",
                                        "author": "Eric Matthes", "translator": None, "genre": None, "year": None,
                                        "publisher": None, "isbn": "978-1593279288"},
                               "hidden": False, "status": "Available for exchange"},
                              {"book": {"id": 2, "name": "Clean Code: A Handbook of Agile Software Craftsmanship",
                                        "author": "Robert C. Martin", "translator": None, "genre": None, "year": None,
                                        "publisher": None, "isbn": "978-0132350884"},
                               "hidden": False, "status": "Available for exchange"}
                              ],
                    'hidden_lib': False, 'id': 1}
        self.assertEqual(201, resp.status_code)
        self.assertEqual(expected, resp.json)

    def test_04_get_non_empty_lib(self):
        resp = app.test_client().get('/users/1/library')
        expected = {'books': [{"book": {"id": 1, "name": "Python Crash Course, 2nd Edition: A Hands-On, "
                                                         "Project-Based Introduction to Programming",
                                        "author": "Eric Matthes", "translator": None, "genre": None, "year": None,
                                        "publisher": None, "isbn": "978-1593279288"},
                               "hidden": False, "status": "Available for exchange"},
                              {"book": {"id": 2, "name": "Clean Code: A Handbook of Agile Software Craftsmanship",
                                        "author": "Robert C. Martin", "translator": None, "genre": None, "year": None,
                                        "publisher": None, "isbn": "978-0132350884"},
                               "hidden": False, "status": "Available for exchange"}
                              ],
                    'hidden_lib': False, 'id': 1}
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)

    def test_05_get_non_existent_users_lib(self):
        resp = app.test_client().get('/users/2/library')
        self.assertEqual(404, resp.status_code)
        self.assertEqual('No such user', resp.json['ErrorMessage'])

    def test_06_post_non_existent_users_lib(self):
        data = json.dumps({'book_id': 2})
        resp = app.test_client().post('/users/2/library', data=data, content_type='application/json')
        self.assertEqual(404, resp.status_code)
        self.assertEqual('No such user', resp.json['ErrorMessage'])

    def test_07_post_excessive_info(self):
        example_book = Book(isbn='978-0134240884',
                            name='Not existing testing book',
                            author='Jane Doe')
        db.session.add(example_book)
        db.session.commit()

        data = json.dumps({'book_id': 3, 'hidden': True})
        resp = app.test_client().post('/users/1/library', data=data, content_type='application/json')
        self.assertEqual(400, resp.status_code)
        self.assertEqual('Excessive arguments posted', resp.json['ErrorMessage'])

    def test_08_hide_lib(self):
        data = json.dumps({'hidden_lib': True})
        resp = app.test_client().patch('/users/1/library', data=data, content_type='application/json')
        expected = {'books': [{"book": {"id": 1, "name": "Python Crash Course, 2nd Edition: A Hands-On, "
                                                         "Project-Based Introduction to Programming",
                                        "author": "Eric Matthes", "translator": None, "genre": None, "year": None,
                                        "publisher": None, "isbn": "978-1593279288"},
                               "hidden": False, "status": "Available for exchange"},
                              {"book": {"id": 2, "name": "Clean Code: A Handbook of Agile Software Craftsmanship",
                                        "author": "Robert C. Martin", "translator": None, "genre": None, "year": None,
                                        "publisher": None, "isbn": "978-0132350884"},
                               "hidden": False, "status": "Available for exchange"}
                              ],
                    'hidden_lib': True, 'id': 1}
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)

        # try again
        resp = app.test_client().patch('/users/1/library', data=data, content_type='application/json')
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)

    def test_09_patch_book_in_lib(self):
        data = json.dumps({'book_id': 2, 'hidden': True, 'status': 'Not available for exchange'})
        resp = app.test_client().patch('/users/1/library', data=data, content_type='application/json')
        expected = {"book": {"id": 2, "name": "Clean Code: A Handbook of Agile Software Craftsmanship",
                                        "author": "Robert C. Martin", "translator": None, "genre": None, "year": None,
                                        "publisher": None, "isbn": "978-0132350884"},
                               "hidden": True, "status": "Not available for exchange"}
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)

        resp = app.test_client().get('/users/1/library')
        expected = {'books': [{"book": {"id": 1, "name": "Python Crash Course, 2nd Edition: A Hands-On, "
                                                         "Project-Based Introduction to Programming",
                                        "author": "Eric Matthes", "translator": None, "genre": None, "year": None,
                                        "publisher": None, "isbn": "978-1593279288"},
                               "hidden": False, "status": "Available for exchange"},
                              {"book": {"id": 2, "name": "Clean Code: A Handbook of Agile Software Craftsmanship",
                                        "author": "Robert C. Martin", "translator": None, "genre": None, "year": None,
                                        "publisher": None, "isbn": "978-0132350884"},
                               "hidden": True, "status": "Not available for exchange"}
                              ],
                    'hidden_lib': True, 'id': 1}
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)

    def test_10_patch_excessive_info(self):
        data = json.dumps({'hidden_lib': True, 'status': 'cool'})
        resp = app.test_client().patch('/users/1/library', data=data, content_type='application/json')
        self.assertEqual(400, resp.status_code)
        self.assertEqual('Excessive arguments posted', resp.json['ErrorMessage'])

        data = json.dumps({'book_id': 2, 'hidden': True, 'status': 'Not available for exchange', 'info': 'great book'})
        resp = app.test_client().patch('/users/1/library', data=data, content_type='application/json')
        self.assertEqual(400, resp.status_code)
        self.assertEqual('Excessive arguments posted', resp.json['ErrorMessage'])

    def test_11_patch_book_not_existent_in_lib(self):
        data = json.dumps({'book_id': 8, 'hidden': True, 'status': 'Not available for exchange'})
        resp = app.test_client().patch('/users/1/library', data=data, content_type='application/json')
        self.assertEqual(404, resp.status_code)
        self.assertEqual('No such book in library', resp.json['ErrorMessage'])

    def test_12_delete_book_from_lib(self):
        resp = app.test_client().delete('/users/1/library/2')
        expected = {'books': [{"book": {"id": 1, "name": "Python Crash Course, 2nd Edition: A Hands-On, "
                                                         "Project-Based Introduction to Programming",
                                        "author": "Eric Matthes", "translator": None, "genre": None, "year": None,
                                        "publisher": None, "isbn": "978-1593279288"},
                               "hidden": False, "status": "Available for exchange"}
                              ],
                    'hidden_lib': True, 'id': 1}
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)

    def test_13_delete_not_existent_book(self):
        resp = app.test_client().delete('/users/1/library/2')
        self.assertEqual(404, resp.status_code)
        self.assertEqual('No such book in user''s library', resp.json['ErrorMessage'])

    def test_14_add_the_same_book(self):
        data = json.dumps({'book_id': 1})
        resp = app.test_client().post('/users/1/library', data=data, content_type='application/json')
        self.assertEqual(403, resp.status_code)
        self.assertEqual('This book is already in library', resp.json['ErrorMessage'])


class TestWishlist(TestCase):
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

    def test_01_get_empty_wishlist(self):
        data = json.dumps({'username': 'petro', 'group': 'admin'})
        app.test_client().post('/users', data=data, content_type='application/json')

        resp = app.test_client().get('/users/1/wishlist')
        self.assertEqual(200, resp.status_code)
        self.assertEqual([], resp.json)

    def test_02_add_book_to_wishlist(self):
        example_book = Book(isbn='978-1593279288',
                            name='Python Crash Course, 2nd Edition: A Hands-On'
                                 ', Project-Based Introduction to Programming',
                            author='Eric Matthes')
        db.session.add(example_book)
        db.session.commit()

        data = json.dumps({'book_id': 1})
        resp = app.test_client().post('/users/1/wishlist', data=data, content_type='application/json')
        expected = [{"id": 1, "name": "Python Crash Course, 2nd Edition: A Hands-On, "
                                      "Project-Based Introduction to Programming",
                     "author": "Eric Matthes", "translator": None, "genre": None, "year": None,
                     "publisher": None, "isbn": "978-1593279288"}]
        self.assertEqual(201, resp.status_code)
        self.assertEqual(expected, resp.json)

    def test_03_add_the_same_book(self):
        data = json.dumps({'book_id': 1})
        resp = app.test_client().post('/users/1/wishlist', data=data, content_type='application/json')
        self.assertEqual(403, resp.status_code)
        self.assertEqual('This book is already in wishlist', resp.json['ErrorMessage'])

    def test_04_get_wishlist(self):
        example_book = Book(isbn='978-0132350884',
                            name='Clean Code: A Handbook of Agile Software Craftsmanship',
                            author='Robert C. Martin')
        db.session.add(example_book)
        db.session.commit()

        data = json.dumps({'book_id': 2})
        app.test_client().post('/users/1/wishlist', data=data, content_type='application/json')
        resp = app.test_client().get('/users/1/wishlist')
        expected = [{"id": 1, "name": "Python Crash Course, 2nd Edition: A Hands-On, "
                                      "Project-Based Introduction to Programming",
                     "author": "Eric Matthes", "translator": None, "genre": None, "year": None,
                     "publisher": None, "isbn": "978-1593279288"},
                    {"id": 2, "name": "Clean Code: A Handbook of Agile Software Craftsmanship",
                     "author": "Robert C. Martin", "translator": None, "genre": None, "year": None,
                     "publisher": None, "isbn": "978-0132350884"}
                    ]
        self.assertEqual(200, resp.status_code)
        self.assertEqual(expected, resp.json)

    def test_05_add_non_existent_book(self):
        data = json.dumps({'book_id': 3})
        resp = app.test_client().post('/users/1/wishlist', data=data, content_type='application/json')
        self.assertEqual(404, resp.status_code)
        self.assertEqual('No such book', resp.json['ErrorMessage'])

    def test_05_add_to_non_existent_user(self):
        data = json.dumps({'book_id': 2})
        resp = app.test_client().post('/users/2/wishlist', data=data, content_type='application/json')
        self.assertEqual(404, resp.status_code)
        self.assertEqual('No such user', resp.json['ErrorMessage'])


if __name__ == '__main__':
    unittest.main()
