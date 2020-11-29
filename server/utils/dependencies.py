from flask_injector import request

from services.EventCommentService import EventCommentService
from services.EventInvitationService import EventInvitationService
from services.UserService import UserService
from validators.EventCommentValidator import EventCommentValidator
from validators.EventInvitationValidator import EventInvitationValidator
from validators.UserValidator import UserValidator
from services.EventService import EventService
from validators.EventValidator import EventValidator


def configure_services(binder):
    user_validator = UserValidator()
    user_service = UserService(user_validator)
    binder.bind(UserService, to=user_service, scope=request)

    event_validator = EventValidator()
    events_service = EventService(event_validator)
    binder.bind(EventService, to=events_service, scope=request)

    event_comment_validator = EventCommentValidator()
    events_comments_service = EventCommentService(event_comment_validator)
    binder.bind(EventCommentService, to=events_comments_service, scope=request)

    event_invitation_validator = EventInvitationValidator()
    event_invitation_service = EventInvitationService(event_invitation_validator)
    binder.bind(EventInvitationService, to=event_invitation_service, scope=request)
