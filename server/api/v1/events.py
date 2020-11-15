from flask import Blueprint, jsonify, request, Flask, Response
from flask_jwt_extended import jwt_required, get_jwt_identity

from models.Event import event_visibility_map, event_category_map, EVENT_VISIBILITY_PUBLIC
from services.EventCommentService import EventCommentService
from services.EventService import EventService
from services.UserService import UserService
from utils.errors import UserDoesNotExist, EventDoesNotExist, EventCommentDoesNotExist

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


def extract_event_comment_properties():
    text = request.json.get('text')
    return text


@api.route('')
def events_get(event_service: EventService):
    events = event_service.find_by(visibility=event_visibility_map.to_key(EVENT_VISIBILITY_PUBLIC))
    return jsonify([event.to_dict() for event in events])


@api.route('/visibilities')
def events_get_visibilities():
    return jsonify(event_visibility_map.to_reverse_dict())


@api.route('/categories')
def events_get_categories():
    return jsonify(event_category_map.to_reverse_dict())


@api.route('', methods=['POST'])
@jwt_required
def events_post(user_service: UserService, event_service: EventService):
    username = get_jwt_identity()
    user = user_service.find_one_by(username=username)
    if user is None:
        raise UserDoesNotExist()

    title, location, location_point, date, description, visibility, category = extract_event_properties()
    event = event_service.add(user, title, location, location_point, date, description, visibility, category)
    return jsonify(event.to_dict())


@api.route('/<string:event_id>')
def events_get_event(event_service: EventService, event_id: str):
    event = event_service.find_one_by(id=event_id)
    if event is None:
        raise EventDoesNotExist()

    return jsonify(event.to_dict())


@api.route('/<string:event_id>', methods=['PATCH'])
@jwt_required
def events_patch_event(user_service: UserService, event_service: EventService, event_id: str):
    username = get_jwt_identity()
    user = user_service.find_one_by(username=username)
    if user is None:
        raise UserDoesNotExist()

    event = event_service.find_one_by(owner=user, id=event_id)
    if event is None:
        raise EventDoesNotExist()

    title, location, location_point, date, description, visibility, category = extract_event_properties()
    event = event_service.update(event, title, location, location_point, date, description, visibility, category)
    return jsonify(event.to_dict())


@api.route('/<string:event_id>', methods=['DELETE'])
@jwt_required
def events_delete_event(user_service: UserService, event_service: EventService, event_id: str):
    username = get_jwt_identity()
    user = user_service.find_one_by(username=username)
    if user is None:
        raise UserDoesNotExist()

    event = event_service.find_one_by(owner=user, id=event_id)
    if event is None:
        raise EventDoesNotExist()

    event_service.delete(event)
    return jsonify(event.to_dict())


@api.route('/<string:event_id>/comments')
@jwt_required
def events_get_event_comments(event_service: EventService, event_comments_service: EventCommentService,
                              event_id: str):
    event = event_service.find_one_by(id=event_id)
    if event is None:
        raise EventDoesNotExist()

    event_comments = event_comments_service.find_by(event_id=event_id)
    return jsonify([event_comment.to_dict() for event_comment in event_comments])


@api.route('/<string:event_id>/comments', methods=['POST'])
@jwt_required
def events_post_event_comments(event_service: EventService, event_comments_service: EventCommentService,
                               user_service: UserService, event_id: str):
    username = get_jwt_identity()
    user = user_service.find_one_by(username=username)
    if user is None:
        raise UserDoesNotExist()

    event = event_service.find_one_by(id=event_id)
    if event is None:
        raise EventDoesNotExist()

    text = extract_event_comment_properties()
    event_comment = event_comments_service.add(user, event, text)

    return jsonify(event_comment.to_dict())


@api.route('/<string:event_id>/comments/<string:comment_id>', methods=['PATCH'])
@jwt_required
def events_patch_event_comment(event_service: EventService, event_comments_service: EventCommentService,
                               user_service: UserService, event_id: str, comment_id: str):
    username = get_jwt_identity()
    user = user_service.find_one_by(username=username)
    if user is None:
        raise UserDoesNotExist()

    event = event_service.find_one_by(id=event_id)
    if event is None:
        raise EventDoesNotExist()

    event_comment = event_comments_service.find_one_by(author=user, event=event, id=comment_id)
    if event_comment is None:
        raise EventCommentDoesNotExist()

    text = extract_event_comment_properties()
    event_comments_service.update(event_comment, text)

    return jsonify(event_comment.to_dict())


@api.route('/<string:event_id>/comments/<string:comment_id>', methods=['DELETE'])
@jwt_required
def events_delete_event_comment(event_service: EventService, event_comments_service: EventCommentService,
                                user_service: UserService, event_id: str, comment_id: str):
    username = get_jwt_identity()
    user = user_service.find_one_by(username=username)
    if user is None:
        raise UserDoesNotExist()

    event = event_service.find_one_by(id=event_id)
    if event is None:
        raise EventDoesNotExist()

    event_comment = event_comments_service.find_one_by(author=user, event=event, id=comment_id)
    if event_comment is None:
        raise EventCommentDoesNotExist()

    event_comments_service.delete(event_comment)

    return jsonify(event_comment.to_dict())


def register_blueprint(app: Flask, prefix: str):
    app.register_blueprint(api, url_prefix=prefix)
