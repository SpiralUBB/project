from flask import Blueprint, jsonify, Flask

from api.v1.user import register_blueprint as register_user_api_blueprint
from api.v1.event import register_blueprint as register_event_api_blueprint

api = Blueprint('api_v1', __name__)


@api.route('/about')
def about():
    return jsonify({
        'description': 'Version 1 API endpoint',
        'version': 1.0,
    })


def register_blueprint(app: Flask, url_prefix: str):
    app.register_blueprint(api, url_prefix=url_prefix)
    register_user_api_blueprint(app, '{}/user'.format(url_prefix))
