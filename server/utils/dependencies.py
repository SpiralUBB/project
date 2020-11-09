from flask_injector import request

from services.UserService import UserService
from validators.UserValidator import UserValidator
from services.EventService import EventService
from validators.EventValidator import EventValidator


def configure_services(binder):
    user_validator = UserValidator()
    user_service = UserService(user_validator)
    binder.bind(UserService, to=user_service, scope=request)

    event_validator = EventValidator()
    event_service = EventService(event_validator)
    binder.bind(EventService, to=event_service, scope=request)
