import json

from flask import request
from flask_restful import Resource, marshal

from source.db import db, Book
from source.structures import book_struct


class BookRes(Resource):
    def get(self, book_id=None):
        if book_id:
            data = db.session.query(Book).get(book_id)
            return marshal(data, book_struct) if data else {'ErrorMessage': 'No such book'}, 200 if data else 404
        return marshal(db.session.query(Book).all(), book_struct), 200

    def post(self):
        data = json.loads(request.data)
        if data.get('name') and data.get('author'):
            try:
                new = Book(**data)
            except TypeError:
                return {'ErrorMessage': 'Excessive arguments posted'}, 400
            db.session.add(new)
            db.session.commit()
            return marshal(db.session.query(Book).all(), book_struct), 201
        return {'ErrorMessage': 'Not enough arguments'}, 400