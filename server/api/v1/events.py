from typing import List

from bson import ObjectId
from flask import Blueprint, jsonify, request, Flask
from flask_jwt_extended import jwt_required, get_jwt_identity, jwt_optional

from models.Event import event_visibility_map, event_category_map, Event
from models.User import User
from services.EventCommentService import EventCommentService
from services.EventInvitationService import EventInvitationService
from services.EventService import EventService
from services.UserService import UserService
from utils.errors import UserDoesNotExist, EventDoesNotExist, EventCommentDoesNotExist, EventInvitationDoesNotExist
from utils.pagination import get_paginated_items_from_qs

api = Blueprint('api_v1_events', __name__)


def extract_event_properties():
    title = request.json.get('title')
    location = request.json.get('location')
    location_point = request.json.get('location_point')
    date = request.json.get('date')
    no_max_participants = request.json.get('no_max_participants')
    description = request.json.get('description')
    visibility = request.json.get('visibility')
    category = request.json.get('category')
    return title, location, location_point, date, no_max_participants, description, visibility, category


def extract_event_comment_properties():
    text = request.json.get('text')
    return text


def event_to_restricted_dict(event: Event, event_service: EventService,
                             user: User, full_details_event_ids: List[ObjectId]):
    with_details = event_service.is_details_visible(event, user, full_details_event_ids)
    return event.to_dict(with_details=with_details)


@api.route('')
@jwt_optional
def events_get(user_service: UserService, event_service: EventService,
               event_invitation_service: EventInvitationService):
    # An user can see public events with full details
    # An user can see whitelisted events with limited details
    # An user that is logged in can see events that he owns
    # An user that is logged in can see events for which he has an accepted invite with full details

    username = get_jwt_identity()
    user = user_service.find_one_by(username=username)
    full_details_event_ids = event_invitation_service.find_accepted_user_invitations_event_ids(user)
    events = event_service.find_visible_for_user(user, full_details_event_ids, show_whitelist=True)

    return jsonify(get_paginated_items_from_qs(events, event_to_restricted_dict, event_service, user,
                                               full_details_event_ids))


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

    title, location, location_point, date, no_max_participants, description, visibility, category \
        = extract_event_properties()
    event = event_service.add(user, title, location, location_point, date, no_max_participants, description, visibility,
                              category)
    return jsonify(event.to_dict(with_details=True))


@api.route('/<string:event_id>')
@jwt_optional
def events_get_event(user_service: UserService, event_service: EventService,
                     event_invitation_service: EventInvitationService, event_id: str):
    # An user can see a whitelisted event with limited details
    # An user can see a public event with full details
    # An user that is logged in can see an unlisted event with limited details. Since an unlisted event is not
    # visible within the events route, this means that the owner needs to share the link to it with people
    # that he wants to let join
    # An user that is logged in can see an event that he owns with full details
    # An user that is logged in can see a whitelisted event for which he has an accepted invite with full details
    # An user that is logged in can see an unlisted event for which he has an accepted invite with full details

    username = get_jwt_identity()
    user = user_service.find_one_by(username=username)
    full_details_event_ids = event_invitation_service.find_accepted_user_invitations_event_ids(user)
    event = event_service.find_one_visible_for_user(user, event_id, full_details_event_ids, show_whitelist=True,
                                                    show_unlisted=user is not None)
    if event is None:
        raise EventDoesNotExist()

    return jsonify(event_to_restricted_dict(event, event_service, user, full_details_event_ids))


@api.route('/<string:event_id>', methods=['PATCH'])
@jwt_required
def events_patch_event(user_service: UserService, event_service: EventService, event_id: str):
    username = get_jwt_identity()
    user = user_service.find_one_by(username=username)
    if user is None:
        raise UserDoesNotExist()

    # Restrict to owner
    event = event_service.find_one_by(owner=user, id=event_id)
    if event is None:
        raise EventDoesNotExist()

    title, location, location_point, date, no_max_participants, description, visibility, category = \
        extract_event_properties()
    event_service.update(event, title, location, location_point, date, description, visibility, category)
    return jsonify(event.to_dict(with_details=True))


@api.route('/<string:event_id>', methods=['DELETE'])
@jwt_required
def events_delete_event(user_service: UserService, event_service: EventService, event_id: str):
    username = get_jwt_identity()
    user = user_service.find_one_by(username=username)
    if user is None:
        raise UserDoesNotExist()

    # Restrict to owner
    event = event_service.find_one_by(owner=user, id=event_id)
    if event is None:
        raise EventDoesNotExist()

    event_service.delete(event)
    return jsonify(event.to_dict(with_details=True))


@api.route('/<string:event_id>/comments')
@jwt_required
def events_get_event_comments(user_service: UserService, event_service: EventService,
                              event_comments_service: EventCommentService, event_id: str):
    # A logged in user can access the comments for an event

    username = get_jwt_identity()
    user = user_service.find_one_by(username=username)
    if user is None:
        raise UserDoesNotExist()

    event = event_service.find_one_by(id=event_id)
    if event is None:
        raise EventDoesNotExist()

    event_comments = event_comments_service.find_by(event=event)
    return jsonify(get_paginated_items_from_qs(event_comments))


@api.route('/<string:event_id>/comments', methods=['POST'])
@jwt_required
def events_post_event_comments(user_service: UserService, event_service: EventService,
                               event_comments_service: EventCommentService, event_id: str):
    # A logged in user can access the comments for an event

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
def events_patch_event_comment(user_service: UserService, event_service: EventService,
                               event_comments_service: EventCommentService, event_id: str, comment_id: str):
    # A logged in user can access the comments for an event

    username = get_jwt_identity()
    user = user_service.find_one_by(username=username)
    if user is None:
        raise UserDoesNotExist()

    event = event_service.find_one_by(id=event_id)
    if event is None:
        raise EventDoesNotExist()

    # Restrict to author
    event_comment = event_comments_service.find_one_by(author=user, event=event, id=comment_id)
    if event_comment is None:
        raise EventCommentDoesNotExist()

    text = extract_event_comment_properties()
    event_comments_service.update(event_comment, text)

    return jsonify(event_comment.to_dict())


@api.route('/<string:event_id>/comments/<string:comment_id>', methods=['DELETE'])
@jwt_required
def events_delete_event_comment(user_service: UserService, event_service: EventService,
                                event_comments_service: EventCommentService, event_id: str, comment_id: str):
    # A logged in user can access the comments for an event

    username = get_jwt_identity()
    user = user_service.find_one_by(username=username)
    if user is None:
        raise UserDoesNotExist()

    event = event_service.find_one_by(id=event_id)
    if event is None:
        raise EventDoesNotExist()

    # Restrict to author
    event_comment = event_comments_service.find_one_by(author=user, event=event, id=comment_id)
    if event_comment is None:
        raise EventCommentDoesNotExist()

    event_comments_service.delete(event_comment)

    return jsonify(event_comment.to_dict())


@api.route('/<string:event_id>/invitation')
@jwt_required
def events_get_event_invitation(user_service: UserService, event_service: EventService,
                                event_invitation_service: EventInvitationService,
                                event_id: str):
    # A logged in user can get his invitation status for an event

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


@api.route('/<string:event_id>/invitation', methods=['PUT'])
@jwt_required
def events_put_event_join(event_service: EventService, event_invitation_service: EventInvitationService,
                          user_service: UserService, event_id: str):
    # A logged in user can join a public event
    # A logged in user can join a whitelisted or unlisted event, the invitation will be marked pending

    username = get_jwt_identity()
    user = user_service.find_one_by(username=username)
    if user is None:
        raise UserDoesNotExist()

    event = event_service.find_one_by(id=event_id)
    if event is None:
        raise EventDoesNotExist()

    event_service.check_can_user_join_event(event, user)
    event_invitation = event_invitation_service.join(event, user)

    return jsonify(event_invitation.to_dict())


@api.route('/<string:event_id>/invitations')
@jwt_required
def events_get_event_invitations(event_service: EventService, event_invitation_service: EventInvitationService,
                                 user_service: UserService, event_id: str):
    # A logged in user can see the accepted invitations for a public event
    # A logged in user can see the accepted invitations for a whitelisted or unlisted event for which he has an
    # accepted invite
    # A logged in user can see the all the invitations for an event that he owns

    username = get_jwt_identity()
    user = user_service.find_one_by(username=username)
    if user is None:
        raise UserDoesNotExist()

    full_details_event_ids = event_invitation_service.find_accepted_user_invitations_event_ids(user)
    event = event_service.find_one_visible_for_user(user, event_id, full_details_event_ids)
    if event is None:
        raise EventDoesNotExist()

    event_invitations = event_invitation_service.find_visible_for_user(user, event)

    return jsonify(get_paginated_items_from_qs(event_invitations, with_user=True))


@api.route('/<string:event_id>/invitations/<string:invitation_id>/accept', methods=['PUT'])
@jwt_required
def events_put_event_invitation_accept(event_service: EventService, event_invitation_service: EventInvitationService,
                                       user_service: UserService, event_id: str, invitation_id: str):
    username = get_jwt_identity()
    user = user_service.find_one_by(username=username)
    if user is None:
        raise UserDoesNotExist()

    # Restrict to owner
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
