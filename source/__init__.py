from flask import Blueprint
from flask_restful import Api

from source.routes.books import BookRes
from source.routes.users import UserRes, AddrRes

routes_bp = Blueprint('routes', __name__)
routes_api = Api(routes_bp)

routes_api.add_resource(UserRes, '/users', '/users/<int:user_id>')
routes_api.add_resource(BookRes, '/books', '/books/<int:book_id>')
routes_api.add_resource(AddrRes, '/addr', '/addr/<int:addr_id>')