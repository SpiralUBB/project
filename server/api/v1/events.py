from typing import List

from bson import ObjectId
from flask import Blueprint, jsonify, request, Flask

from api.v1.helpers import retrieve_logged_in_user, EventRetrievalType, retrieve_event, ShowFlagType, \
    EventCommentRetrievalType, retrieve_event_comment, EventInvitationRetrievalType, retrieve_event_invitation
from models.Event import event_visibility_map, event_category_map, Event
from models.EventInvitation import event_invitation_status_map, event_invitation_attend_status_map
from models.User import User
from services.EventCommentService import EventCommentService
from services.EventInvitationService import EventInvitationService
from services.EventService import EventService
from utils.dependencies import services_injector
from utils.pagination import get_paginated_items_from_qs

api = Blueprint('api_v1_events', __name__)


def extract_event_properties():
    title = request.json.get('title')
    location = request.json.get('location')
    location_point = request.json.get('location_point')
    start_time = request.json.get('start_time')
    end_time = request.json.get('end_time')
    min_trust_level = request.json.get('min_trust_level')
    no_max_participants = request.json.get('no_max_participants')
    description = request.json.get('description')
    visibility = request.json.get('visibility')
    category = request.json.get('category')
    return title, location, location_point, start_time, end_time, min_trust_level, no_max_participants, description, \
           visibility, category


def extract_event_comment_properties():
    text = request.json.get('text')
    return text


def extract_event_invitation_properties():
    status = request.json.get('status')
    attend_status = request.json.get('attend_status')
    return status, attend_status


def event_to_restricted_dict(event: Event, user: User, full_details_event_ids: List[ObjectId]):
    event_service = services_injector.get(EventService)
    with_details = event_service.is_details_visible(event, user, full_details_event_ids)
    return event.to_dict(with_details=with_details)


@api.route('/visibilities')
def events_get_visibilities():
    return jsonify(event_visibility_map.to_reverse_dict())


@api.route('/categories')
def events_get_categories():
    return jsonify(event_category_map.to_reverse_dict())


@api.route('/invitation_statuses')
def events_get_invitation_statuses():
    return jsonify(event_invitation_status_map.to_reverse_dict())


@api.route('/invitation_attend_statuses')
def events_get_invitation_attend_statuses():
    return jsonify(event_invitation_attend_status_map.to_reverse_dict())


@api.route('')
@retrieve_logged_in_user(optional=True)
def events_get(event_service: EventService, event_invitation_service: EventInvitationService):
    # An user can see public events with full details
    # An user can see whitelisted events with limited details
    # A logged in user can see events that he owns with full details
    # A logged in user can see events for which he has an invite with limited details
    # A logged in user can see events for which he has an accepted invite with full details
    categories = request.args.getlist('category')
    date_start = request.args.get('date_start')
    date_end = request.args.get('date_end')
    invitation_statuses = request.args.getlist('invitation_status')
    invitation_attend_statuses = request.args.getlist('invitation_attend_status')
    own = request.args.get('own')
    user = request.user
    filter_owner = None
    invited_event_ids = None
    filter_event_ids = None

    if own:
        filter_owner = user

    if user:
        invited_event_ids = event_invitation_service.find_for_user_status_event_ids(user)

    if invitation_statuses:
        filter_event_ids = \
            event_invitation_service.find_for_user_status_event_ids(user, statuses=invitation_statuses,
                                                                    attend_statuses=invitation_attend_statuses)

    events = event_service.find_visible_for_user(user, invited_event_ids, show_public=True, show_whitelist=True,
                                                 categories=categories, date_start=date_start, date_end=date_end,
                                                 filter_ids=filter_event_ids, filter_owner=filter_owner)

    full_details_event_ids = event_invitation_service.find_accepted_user_invitations_event_ids(user)
    return jsonify(get_paginated_items_from_qs(events, event_to_restricted_dict, user, full_details_event_ids))


@api.route('', methods=['POST'])
@retrieve_logged_in_user()
def events_post(event_service: EventService):
    title, location, location_point, start_time, end_time, min_trust_level, no_max_participants, description, \
        visibility, category = extract_event_properties()
    user = request.user

    event = event_service.add(user, title, location, location_point, start_time, end_time, min_trust_level,
                              no_max_participants, description, visibility, category)

    return jsonify(event.to_dict(with_details=True))


@api.route('/<string:event_id>')
@retrieve_logged_in_user(optional=True)
@retrieve_event(EventRetrievalType.ID_AND_LOGGED_IN_USER_VISIBLE, show_public=True, show_whitelisted=True,
                show_unlisted=ShowFlagType.USER_EXISTS)
def events_get_event(event_invitation_service: EventInvitationService):
    event = request.event
    user = request.user

    full_details_event_ids = event_invitation_service.find_accepted_user_invitations_event_ids(user)
    return jsonify(event_to_restricted_dict(event, user, full_details_event_ids))


@api.route('/<string:event_id>', methods=['PATCH'])
@retrieve_logged_in_user()
@retrieve_event(EventRetrievalType.ID_AND_OWNER)
def events_patch_event(event_service: EventService):
    title, location, location_point, start_time, end_time, min_trust_level, no_max_participants, description, \
        visibility, category = extract_event_properties()
    event = request.event

    event_service.update(event, title, location, location_point, start_time, end_time, min_trust_level,
                         no_max_participants, description, visibility, category)

    return jsonify(event.to_dict(with_details=True))


@api.route('/<string:event_id>', methods=['DELETE'])
@retrieve_logged_in_user()
@retrieve_event(EventRetrievalType.ID_AND_OWNER)
def events_delete_event(event_service: EventService):
    event = request.event

    event_service.delete(event)

    return jsonify(event.to_dict(with_details=True))


@api.route('/<string:event_id>/comments')
@retrieve_logged_in_user()
@retrieve_event(EventRetrievalType.ID)
def events_get_event_comments(event_comments_service: EventCommentService):
    event = request.event

    event_comments = event_comments_service.find_by(event=event)

    return jsonify(get_paginated_items_from_qs(event_comments))


@api.route('/<string:event_id>/comments', methods=['POST'])
@retrieve_logged_in_user()
@retrieve_event(EventRetrievalType.ID)
def events_post_event_comments(event_comments_service: EventCommentService):
    text = extract_event_comment_properties()
    user = request.user
    event = request.event

    event_comment = event_comments_service.add(user, event, text)

    return jsonify(event_comment.to_dict())


@api.route('/<string:event_id>/comments/<string:comment_id>', methods=['PATCH'])
@retrieve_logged_in_user()
@retrieve_event(EventRetrievalType.ID)
@retrieve_event_comment(EventCommentRetrievalType.ID_AND_AUTHOR)
def events_patch_event_comment(event_comments_service: EventCommentService):
    text = extract_event_comment_properties()
    event_comment = request.event_comment

    event_comments_service.update(event_comment, text)

    return jsonify(event_comment.to_dict())


@api.route('/<string:event_id>/comments/<string:comment_id>', methods=['DELETE'])
@retrieve_logged_in_user()
@retrieve_event(EventRetrievalType.ID)
@retrieve_event_comment(EventCommentRetrievalType.ID_AND_AUTHOR)
def events_delete_event_comment(event_comments_service: EventCommentService):
    event_comment = request.event_comment

    event_comments_service.delete(event_comment)

    return jsonify(event_comment.to_dict())


@api.route('/<string:event_id>/invitation')
@retrieve_logged_in_user()
@retrieve_event(EventRetrievalType.ID)
@retrieve_event_invitation(EventInvitationRetrievalType.LOGGED_IN_USER)
def events_get_event_invitation():
    event_invitation = request.event_invitation
    return jsonify(event_invitation.to_dict())


@api.route('/<string:event_id>/invitation', methods=['PUT'])
@retrieve_logged_in_user()
@retrieve_event(EventRetrievalType.ID)
def events_put_event_join(event_invitation_service: EventInvitationService):
    user = request.user
    event = request.event

    event_invitation = event_invitation_service.add(event, user)

    return jsonify(event_invitation.to_dict())


@api.route('/<string:event_id>/invitations')
@retrieve_logged_in_user()
@retrieve_event(EventRetrievalType.ID_AND_LOGGED_IN_USER_VISIBLE)
def events_get_event_invitations(event_invitation_service: EventInvitationService):
    user = request.user
    event = request.event

    event_invitations = event_invitation_service.find_visible_for_user(user, event)

    return jsonify(get_paginated_items_from_qs(event_invitations, with_user=True))


@api.route('/<string:event_id>/invitations/<string:invitation_id>', methods=['PATCH'])
@retrieve_logged_in_user()
@retrieve_event(EventRetrievalType.ID_AND_OWNER)
@retrieve_event_invitation(EventInvitationRetrievalType.ID)
def events_patch_event_invitation(event_invitation_service: EventInvitationService):
    status, attend_status = extract_event_invitation_properties()
    event_invitation = request.event_invitation

    event_invitation_service.update(event_invitation, status=status, attend_status=attend_status)

    return jsonify(event_invitation.to_dict(with_user=True))


def register_blueprint(app: Flask, prefix: str):
    app.register_blueprint(api, url_prefix=prefix)
