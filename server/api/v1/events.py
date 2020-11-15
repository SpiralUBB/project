from flask import Blueprint, jsonify, request, Flask, Response
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.Event import event_visibility_map, event_category_map
from services.EventsService import EventsService
from services.UserService import UserService
from utils.errors import UserDoesNotExist, EventDoesNotExist

api = Blueprint('api_v1_events', __name__)


def extract_event_properties():
    title = request.json.get('title')
    location = request.json.get('location')
    location_point = request.json.get('location_point')
    date = request.json.get('date')
    description = request.json.get('description')
    visibility = request.json.get('visibility')
    category = request.json.get('category')
    return title, location, location_point, date, description, visibility, category


@api.route('')
def events_get(service: EventsService):
    events = service.find_all()
    return jsonify([event.to_dict() for event in events])


@api.route('/visibilities')
def events_get_visibilities():
    return jsonify(event_visibility_map.to_reverse_dict())


@api.route('/categories')
def events_get_categories():
    return jsonify(event_category_map.to_reverse_dict())


@api.route('', methods=['POST'])
@jwt_required
def events_post(user_service: UserService, events_service: EventsService):
    username = get_jwt_identity()
    user = user_service.find_by(username=username)
    if user is None:
        raise UserDoesNotExist()

    title, location, location_point, date, description, visibility, category = extract_event_properties()
    event = events_service.add(user, title, location, location_point, date, description, visibility, category)
    return jsonify(event.to_dict())


@api.route('/<string:event_id>')
def events_get_event(events_service: EventsService, event_id: str):
    event = events_service.find_by(event_id=event_id)
    if event is None:
        raise EventDoesNotExist()

    return jsonify(event.to_dict())


@api.route('/<string:event_id>', methods=['PATCH'])
@jwt_required
def events_patch_event(user_service: UserService, events_service: EventsService, event_id: str):
    username = get_jwt_identity()
    user = user_service.find_by(username=username)
    if user is None:
        raise UserDoesNotExist()

    event = events_service.find_by(owner=user, event_id=event_id)
    if event is None:
        raise EventDoesNotExist()

    title, location, location_point, date, description, visibility, category = extract_event_properties()
    event = events_service.update(event, title, location, location_point, date, description, visibility, category)
    return jsonify(event.to_dict())


@api.route('/<string:event_id>', methods=['DELETE'])
@jwt_required
def events_delete_event(user_service: UserService, events_service: EventsService, event_id: str):
    username = get_jwt_identity()
    user = user_service.find_by(username=username)
    if user is None:
        raise UserDoesNotExist()

    event = events_service.find_by(owner=user, event_id=event_id)
    if event is None:
        raise EventDoesNotExist()

    events_service.delete(event)
    return jsonify(event.to_dict())


def register_blueprint(app: Flask, prefix: str):
    app.register_blueprint(api, url_prefix=prefix)
