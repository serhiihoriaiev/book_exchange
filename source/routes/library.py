import json

import sqlalchemy
from flask import request
from flask_restful import Resource, marshal
from sqlalchemy import and_

from source.db import db, Library, Book, LibBooks, SiteUser
from source.structures import library_struct, libbook_struct


class LibraRes(Resource):
    def get(self, user_id):
        if db.session.query(SiteUser).get(user_id):
            data = db.session.query(Library).filter(Library.user_id == user_id).first()
            return marshal(data, library_struct), 200
        return {'ErrorMessage': 'No such user'}, 404

    def post(self, user_id):
        if db.session.query(SiteUser).get(user_id):
            data = json.loads(request.data)
            if data.get('book_id'):
                if len(data.keys()) > 1:
                    return {'ErrorMessage': 'Excessive arguments posted'}, 400
                lib = db.session.query(Library).filter(Library.user_id == user_id).first()
                book = db.session.query(Book).get(data.get('book_id'))
                if book:
                    if db.session.query(LibBooks).filter(and_(LibBooks.lib_id == lib.id, LibBooks.book_id == book.id)).first():
                        return {'ErrorMessage': 'This book is already in library'}, 403
                    lb = LibBooks()
                    lb.book = book
                    lib.books.append(lb)
                    db.session.commit()
                    return marshal(lib, library_struct), 201
                return {'ErrorMessage': 'No such book'}, 404
            return {'ErrorMessage': 'Book not specified'}, 400
        return {'ErrorMessage': 'No such user'}, 404

    def patch(self, user_id):
        if db.session.query(SiteUser).get(user_id):
            data = json.loads(request.data)
            if data.get('book_id'):
                bid = data.pop('book_id')
                lid = db.session.query(Library).filter(Library.user_id == user_id).first().id
                if not db.session.query(LibBooks).filter(and_(LibBooks.lib_id == lid, LibBooks.book_id == bid)).first():
                    return {'ErrorMessage': 'No such book in library'}, 404
                try:
                    db.session.query(LibBooks).filter(and_(LibBooks.lib_id == lid, LibBooks.book_id == bid)).update(
                        data)
                except sqlalchemy.exc.InvalidRequestError:
                    return {'ErrorMessage': 'Excessive arguments posted'}, 400
                db.session.commit()
                return marshal(
                    db.session.query(LibBooks).filter(and_(LibBooks.lib_id == lid, LibBooks.book_id == bid)).first(),
                    libbook_struct
                ), 200
            if data.get('hidden_lib'):
                if data.get('id'):
                    return {'ErrorMessage': 'You can''t change ID'}, 403
                if len(data.keys()) > 1:
                    return {'ErrorMessage': 'Excessive arguments posted'}, 400
                db.session.query(Library).filter(Library.user_id == user_id).update(data)
                db.session.commit()
                return marshal(db.session.query(Library).filter(Library.user_id == user_id).first(), library_struct), 200
        return {'ErrorMessage': 'No such user'}, 404

    def delete(self, user_id, book_id=None):
        if db.session.query(SiteUser).get(user_id):
            if book_id:
                lid = db.session.query(Library).filter(Library.user_id == user_id).first().id
                b = db.session.query(LibBooks).filter(and_(LibBooks.lib_id == lid, LibBooks.book_id == book_id)).first()
                if b:
                    db.session.delete(b)
                    db.session.commit()
                    return marshal(db.session.query(Library).filter(Library.user_id == user_id).first(), library_struct), 200
                return {'ErrorMessage': 'No such book in user''s library'}, 404
            return {'ErrorMessage': 'Book not specified'}, 400
        return {'ErrorMessage': 'No such user'}, 404