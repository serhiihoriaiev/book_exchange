import json

from flask import request
from flask_restful import Resource, marshal

from source.db import db, Book
from source.db import SiteUser
from source.structures import book_struct


class WishRes(Resource):
    def get(self, user_id):
        if db.session.query(SiteUser).get(user_id):
            data = db.session.query(SiteUser).get(user_id).wishlist
            return marshal(data, book_struct), 200
        return {'ErrorMessage': 'No such user'}, 404

    def post(self, user_id):
        if db.session.query(SiteUser).get(user_id):
            data = json.loads(request.data)
            if data.get('book_id'):
                user = db.session.query(SiteUser).get(user_id)
                book = db.session.query(Book).get(data.get('book_id'))
                if book:
                    if book in user.wishlist:
                        return {'ErrorMessage': 'This book is already in wishlist'}, 403
                    user.wishlist.append(book)
                    db.session.commit()
                    return marshal(user.wishlist, book_struct), 201
                return {'ErrorMessage': 'No such book'}, 404
            return {'ErrorMessage': 'Book not specified'}, 400
        return {'ErrorMessage': 'No such user'}, 404

    def delete(self, user_id, book_id=None):
        if db.session.query(SiteUser).get(user_id):
            if book_id:
                user = db.session.query(SiteUser).get(user_id)
                book = db.session.query(Book).get(book_id)
                if book in user.wishlist:
                    user.wishlist.remove(book)
                    db.session.commit()
                    return marshal(user.wishlist, book_struct), 200
                return {'ErrorMessage': 'No such book in wishlist'}, 404
            return {'ErrorMessage': 'Book not specified'}, 400
        return {'ErrorMessage': 'No such user'}, 404