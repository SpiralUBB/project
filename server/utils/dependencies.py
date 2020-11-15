from flask_injector import request

from services.EventCommentsService import EventCommentsService
from services.UserService import UserService
from validators.EventCommentValidator import EventCommentValidator
from validators.UserValidator import UserValidator
from services.EventsService import EventsService
from validators.EventValidator import EventValidator


def configure_services(binder):
    user_validator = UserValidator()
    user_service = UserService(user_validator)
    binder.bind(UserService, to=user_service, scope=request)

    event_validator = EventValidator()
    events_service = EventsService(event_validator)
    binder.bind(EventsService, to=events_service, scope=request)

    event_comment_validator = EventCommentValidator()
    events_comments_service = EventCommentsService(event_comment_validator)
    binder.bind(EventCommentsService, to=events_comments_service, scope=request)
