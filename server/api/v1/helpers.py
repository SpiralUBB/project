from functools import wraps

from flask import request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request_optional, verify_jwt_in_request

from services.UserService import UserService
from utils.dependencies import services_injector
from utils.errors import UserNotLoggedIn, UserLoggedInInvalid


def retrieve_logged_in_user(optional=False):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            request.user = None

            if optional:
                verify_jwt_in_request_optional()
            else:
                verify_jwt_in_request()

            username = get_jwt_identity()
            if not username:
                if optional:
                    return
                else:
                    raise UserNotLoggedIn()

            user_service = services_injector.get(UserService)
            user = user_service.find_one_by(username=username)
            if not user:
                raise UserLoggedInInvalid()

            request.user = user

            return fn(*args, **kwargs)

        return wrapper

    return decorator
