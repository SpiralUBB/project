from enum import Enum
from functools import wraps
from typing import Union

from flask import request
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request_optional, verify_jwt_in_request

from models.User import User
from services.EventCommentService import EventCommentService
from services.EventInvitationService import EventInvitationService
from services.EventService import EventService
from services.UserService import UserService
from utils.dependencies import services_injector
from utils.errors import UserNotLoggedIn, UserLoggedInInvalid, EventDoesNotExist, EventCommentDoesNotExist, \
    EventInvitationDoesNotExist


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


class EventRetrievalType(Enum):
    ID = 1
    ID_AND_OWNER = 2
    ID_AND_LOGGED_IN_USER_VISIBLE = 4


class ShowFlagType(Enum):
    USER_EXISTS = 1


def parse_show_flag(flag: Union[bool, ShowFlagType] = False, user: User = None):
    if flag == ShowFlagType.USER_EXISTS:
        return user is not None

    return flag


def retrieve_event(retrieval_type: EventRetrievalType,
                   show_public: Union[bool, ShowFlagType] = False,
                   show_whitelisted: Union[bool, ShowFlagType] = False,
                   show_unlisted: Union[bool, ShowFlagType] = False):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = request.user

            request.event = None

            event_id = kwargs.pop('event_id')
            if not event_id:
                raise EventDoesNotExist()

            event_service = services_injector.get(EventService)
            event_invitation_service = services_injector.get(EventInvitationService)
            if retrieval_type == EventRetrievalType.ID:
                event = event_service.find_one_by(id=event_id)
            elif retrieval_type == EventRetrievalType.ID_AND_LOGGED_IN_USER_VISIBLE:
                invited_event_ids = event_invitation_service.find_for_user_status_event_ids(user)
                i_show_public = parse_show_flag(show_public, user)
                i_show_whitelisted = parse_show_flag(show_whitelisted, user)
                i_show_unlisted = parse_show_flag(show_unlisted, user)
                event = event_service.find_one_visible_for_user(user, event_id, invited_event_ids,
                                                                show_public=i_show_public,
                                                                show_whitelist=i_show_whitelisted,
                                                                show_unlisted=i_show_unlisted)
            elif retrieval_type == EventRetrievalType.ID_AND_OWNER:
                event = event_service.find_one_by(owner=user, id=event_id)
            else:
                event = None

            if event is None:
                raise EventDoesNotExist()

            request.event = event

            return fn(*args, **kwargs)

        return wrapper

    return decorator


class EventCommentRetrievalType(Enum):
    ID_AND_AUTHOR = 1


def retrieve_event_comment(retrieval_type: EventCommentRetrievalType):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = request.user
            event = request.event

            request.event_comment = None

            comment_id = kwargs.pop('comment_id')
            if not comment_id:
                raise EventCommentDoesNotExist()

            event_comment_service = services_injector.get(EventCommentService)
            if retrieval_type == EventCommentRetrievalType.ID_AND_AUTHOR:
                event_comment = event_comment_service.find_one_by(author=user, event=event, id=comment_id)
            else:
                event_comment = None

            if event_comment is None:
                raise EventCommentDoesNotExist()

            request.event_comment = event_comment

            return fn(*args, **kwargs)

        return wrapper

    return decorator


class EventInvitationRetrievalType(Enum):
    ID = 1
    LOGGED_IN_USER = 2


def retrieve_event_invitation(retrieval_type: EventInvitationRetrievalType):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = request.user
            event = request.event

            request.event_invitation = None

            event_invitation_service = services_injector.get(EventInvitationService)
            if retrieval_type == EventInvitationRetrievalType.ID:
                invitation_id = kwargs.pop('invitation_id')
                if not invitation_id:
                    raise EventCommentDoesNotExist()

                event_invitation = event_invitation_service.find_one_by(id=invitation_id, event=event)
            elif retrieval_type == EventInvitationRetrievalType.LOGGED_IN_USER:
                event_invitation = event_invitation_service.find_one_by(user=user, event=event)
            else:
                event_invitation = None

            if event_invitation is None:
                raise EventInvitationDoesNotExist()

            request.event_invitation = event_invitation

            return fn(*args, **kwargs)

        return wrapper

    return decorator
