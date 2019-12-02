from unittest import TestCase

from db import db
from main import create_app

app = create_app('TEST')


class TestBooksExchange(TestCase):
    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.drop_all()
        db.session.commit()
