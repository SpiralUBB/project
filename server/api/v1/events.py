from flask import Blueprint, jsonify, request, Flask
from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_optional

from models.Event import event_visibility_map, event_category_map, EVENT_VISIBILITY_WHITELIST, Event, \
    EVENT_VISIBILITY_PRIVATE, EVENT_VISIBILITY_PUBLIC
from models.EventInvitation import event_invitation_status_map, EVENT_INVITATION_STATUS_ACCEPTED, EventInvitation
from services.EventCommentService import EventCommentService
from services.EventInvitationService import EventInvitationService
from services.EventService import EventService
from services.UserService import UserService
from utils.errors import UserDoesNotExist, EventDoesNotExist, EventCommentDoesNotExist, EventInvitationCannotJoinOwn, \
    EventInvitationCannotJoinPrivate, EventInvitationStatusInvalid, EventInvitationDoesNotExist
from utils.pagination import get_paginated_items_from_qs

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
@jwt_optional
def events_get(user_service: UserService, event_service: EventService,
               event_invitation_service: EventInvitationService):
    username = get_jwt_identity()

    if username:
        user = user_service.find_one_by(username=username)
        accepted_event_invitations = event_invitation_service.find_by(
            user=user,
            status=event_invitation_status_map.to_key(EVENT_INVITATION_STATUS_ACCEPTED)
        )
    else:
        user = None
        accepted_event_invitations = []

    event_ids = [ei.id for ei in accepted_event_invitations]
    events = event_service.find_visible_for_user(user, event_ids)

    def event_mapping(event: Event):
        # For whitelisted events for which the user doesn't have an accepted invite,
        # and for which the user isn't the owner, we need to restrict the information shown
        hide_details = event_visibility_map.to_key(EVENT_VISIBILITY_WHITELIST) == event.visibility \
                       and event.id not in event_ids and event.owner.id != user.id
        return event.to_dict(hide_details)

    return jsonify(get_paginated_items_from_qs(events, mapping_fn=event_mapping))


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

    event_comments = event_comments_service.find_by(id=event_id)
    return jsonify(get_paginated_items_from_qs(event_comments))


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


@api.route('/<string:event_id>/join', methods=['PUT'])
@jwt_required
def events_put_event_join(event_service: EventService, event_invitation_service: EventInvitationService,
                          user_service: UserService, event_id: str):
    username = get_jwt_identity()
    user = user_service.find_one_by(username=username)
    if user is None:
        raise UserDoesNotExist()

    event = event_service.find_one_by(id=event_id)
    if event is None:
        raise EventDoesNotExist()

    if event.owner.id == user.id:
        raise EventInvitationCannotJoinOwn()

    if event.visibility == event_visibility_map.to_key(EVENT_VISIBILITY_PRIVATE):
        raise EventInvitationCannotJoinPrivate()

    if event.visibility == event_visibility_map.to_key(EVENT_VISIBILITY_WHITELIST):
        event_invitation = event_invitation_service.add(event, user)
    elif event.visibility == event_visibility_map.to_key(EVENT_VISIBILITY_PUBLIC):
        event_invitation = event_invitation_service.add(event, user, True)
    else:
        raise EventInvitationStatusInvalid()

    return jsonify(event_invitation.to_dict())


@api.route('/<string:event_id>/invitation')
@jwt_required
def events_get_event_invitation(event_service: EventService, event_invitation_service: EventInvitationService,
                                user_service: UserService, event_id: str):
    username = get_jwt_identity()
    user = user_service.find_one_by(username=username)
    if user is None:
        raise UserDoesNotExist()

    event = event_service.find_one_by(id=event_id)
    if event is None:
        raise EventDoesNotExist()

    event_invitation = event_invitation_service.find_one_by(user=user, event=event)
    if event_invitation is None:
        raise EventInvitationDoesNotExist()

    return jsonify(event_invitation.to_dict())


@api.route('/<string:event_id>/invitations')
@jwt_required
def events_get_event_invitations(event_service: EventService, event_invitation_service: EventInvitationService,
                                 user_service: UserService, event_id: str):
    username = get_jwt_identity()
    user = user_service.find_one_by(username=username)
    if user is None:
        raise UserDoesNotExist()

    event = event_service.find_one_by(id=event_id)
    if event is None:
        raise EventDoesNotExist()

    if event.owner.id == user.id:
        status = None
    else:
        status = event_invitation_status_map.to_key(EVENT_INVITATION_STATUS_ACCEPTED)

    event_invitations = event_invitation_service.find_by(status=status)

    return jsonify(get_paginated_items_from_qs(event_invitations, with_user=True))


@api.route('/<string:event_id>/invitations/<string:invitation_id>/accept', methods=['PUT'])
@jwt_required
def events_put_event_invitation_accept(event_service: EventService, event_invitation_service: EventInvitationService,
                                       user_service: UserService, event_id: str, invitation_id: str):
    username = get_jwt_identity()
    user = user_service.find_one_by(username=username)
    if user is None:
        raise UserDoesNotExist()

    event = event_service.find_one_by(id=event_id, owner=user)
    if event is None:
        raise EventDoesNotExist()

    event_invitation = event_invitation_service.find_one_by(id=invitation_id, event=event)
    if event_invitation is None:
        raise EventInvitationDoesNotExist()

    event_invitation_service.accept(event_invitation)

    return jsonify(event_invitation.to_dict(with_user=True))


def register_blueprint(app: Flask, prefix: str):
    app.register_blueprint(api, url_prefix=prefix)
