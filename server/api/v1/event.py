from flask import Blueprint, jsonify, request, Flask, Response
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, get_jwt_identity, \
    unset_access_cookies

from services.EventService import EventService
from utils.errors import EventDoesNotExist, AddEventFailed

api = Blueprint('api_v1_event', __name__)


@api.route('')
@jwt_required
def user_get(service: EventService):
    id = get_jwt_identity()
    event = service.find_by(id=id)
    if event is None:
        raise EventDoesNotExist()

    return jsonify(event.to_dict())


@api.route('/addEvent', methods=['POST'])
def event_post(service: EventService):
    id = request.json.get('id')
    username = request.json.get('username')
    title = request.json.get('title')
    location = request.json.get('location')
    date = request.json.get('date')
    description = request.json.get('description')
    privacy = request.json.get('privacy')
    type = request.json.get('type')

    event = service.add(id, username, title, location, date, description, privacy, type)
    return jsonify(event.to_dict())


def register_blueprint(app: Flask, prefix: str):
    app.register_blueprint(api, url_prefix=prefix)
