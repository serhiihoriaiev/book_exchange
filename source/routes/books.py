import json

import sqlalchemy
from flask import request
from flask_restful import Resource, marshal

from source.db import db, Book, LibBooks, SiteUser
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

    def patch(self, book_id=None):
        if book_id:
            data = json.loads(request.data)
            if data.get('id'):
                return {'ErrorMessage': "You can't change ID"}, 403
            if db.session.query(Book).get(book_id):
                try:
                    db.session.query(Book).filter(Book.id == book_id).update(data)
                except sqlalchemy.exc.InvalidRequestError:
                    return {'ErrorMessage': 'Excessive arguments posted'}, 400
                db.session.commit()
                return marshal(db.session.query(Book).get(book_id), book_struct), 200
        return {'ErrorMessage': 'Book not specified'}, 400

    def delete(self, book_id=None):
        if book_id:
            book = db.session.query(Book).get(book_id)
            if book:
                # we also need to deleted this book from all the libraries
                lib_books = db.session.query(LibBooks).filter(LibBooks.book_id == book_id).all()
                for lb in lib_books:
                    db.session.delete(lb)

                # delete from wishlists
                wl_users = db.session.query(SiteUser).filter(SiteUser.wishlist.contains(book))
                for wu in wl_users:
                    wu.wishlist.remove(book)

                db.session.delete(book)
                db.session.commit()
                return marshal(db.session.query(Book).order_by(Book.id).all(), book_struct), 200
            return {'ErrorMessage': 'No such book'}, 404
        return {'ErrorMessage': 'Book not specified'}, 400