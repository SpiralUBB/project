from flask import Blueprint, jsonify, Flask

from api.v1.user import register_blueprint as register_user_api_blueprint
from api.v1.events import register_blueprint as register_events_api_blueprint
from api.v1.feedbacks import register_blueprint as register_feedbacks_api_blueprint

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
    register_events_api_blueprint(app, '{}/events'.format(url_prefix))
    register_feedbacks_api_blueprint(app, '{}/feedbacks'.format(url_prefix))
