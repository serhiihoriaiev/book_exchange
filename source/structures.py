from flask_restful import fields

address_struct = {
    "id": fields.Integer, "street_addr": fields.String, "city": fields.String,
    "region": fields.String, "zip": fields.String, "country": fields.String
}

book_struct = {
    "id": fields.Integer, "name": fields.String, "author": fields.String, "translator": fields.String,
    "genre": fields.String, "year": fields.Integer(default=None), "publisher": fields.String, "isbn": fields.String

}

library_struct = {
    "id": fields.Integer, "books": fields.Nested(book_struct)
}

user_struct = {
    "id": fields.Integer, "username": fields.String, "group": fields.String,
    "address": fields.Nested(address_struct, default={}), "library": fields.Nested(library_struct, default=[]),
    "wishlist": fields.Nested(book_struct, default=[])
}