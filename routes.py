from flask import Blueprint, render_template

routes_bp = Blueprint('routes', __name__)


@routes_bp.route('/')
def main_page():
    return render_template('main.html')
