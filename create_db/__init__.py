from flask import Blueprint
from flask_restful import Api

from create_db.routes import CreateDBRes

create_db_bp = Blueprint('create_db', __name__)
create_db_api = Api(create_db_bp)

create_db_api.add_resource(CreateDBRes)