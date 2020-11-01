from flask_injector import request

from services.UserService import UserService
from validators.UserValidator import UserValidator


def configure_services(binder):
    user_validator = UserValidator()
    user_service = UserService(user_validator)
    binder.bind(UserService, to=user_service, scope=request)

