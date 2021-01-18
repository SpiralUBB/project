from flask import Blueprint, Flask, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.v1.helpers import retrieve_logged_in_user
from services.EventInvitationService import EventInvitationService
from services.EventService import EventService
from services.UserFeedbackService import UserFeedbackService
from services.UserService import UserService
from utils.errors import UserDoesNotExist, EventDoesNotExist, UserFeedbackAlreadyExists, UserFeedbackDoesNotExist, \
    UserFeedbackCannotGiveOwn

api = Blueprint('api_v1_feedbacks', __name__)


@api.route('', methods=['PUT'])
@retrieve_logged_in_user()
def feedbacks_put_feedback(user_service: UserService, event_service: EventService,
                           event_invitation_service: EventInvitationService,
                           user_feedback_service: UserFeedbackService):
    username = get_jwt_identity()
    user = user_service.find_one_by(username=username)
    if user is None:
        raise UserDoesNotExist()

    to_user_username = request.args.get('to_user')
    if not to_user_username:
        raise UserDoesNotExist()

    to_user = user_service.find_one_by(username=to_user_username)
    if not to_user:
        raise UserDoesNotExist()

    if user.id == to_user.id:
        raise UserFeedbackCannotGiveOwn()

    event_id = request.args.get('event_id')
    if event_id is None:
        event = None
    else:
        # Both users must have an accepted invite to the event this feedback is tied to
        full_details_event_ids = event_invitation_service.find_accepted_user_invitations_event_ids(user)
        event = event_service.find_one_visible_for_user(user, event_id, full_details_event_ids)
        if event is None:
            raise EventDoesNotExist()

        full_details_event_ids = event_invitation_service.find_accepted_user_invitations_event_ids(to_user)
        event = event_service.find_one_visible_for_user(to_user, event_id, full_details_event_ids)
        if event is None:
            raise EventDoesNotExist()

    points = request.json.get('points')
    message = request.json.get('message')

    try:
        user_feedback = user_feedback_service.add(user, to_user, event, points, message)
    except UserFeedbackAlreadyExists:
        user_feedback = user_feedback_service.find_one_by(from_user=user, to_user=to_user, event=event)
        user_feedback_service.update(user_feedback, points=points, message=message)

    return jsonify(user_feedback.to_dict(with_to_user=True, with_event=True))


def register_blueprint(app: Flask, prefix: str):
    app.register_blueprint(api, url_prefix=prefix)
