from flask import Blueprint
from flask_restful import Api

from source.routes.users import UserRes

routes_bp = Blueprint('routes', __name__)
routes_api = Api(routes_bp)

routes_api.add_resource(UserRes, '/users', '/users/<int:user_id>')