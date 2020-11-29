from typing import Union

from mongoengine import DoesNotExist

from models.EventInvitation import EVENT_INVITATION_ATTEND_STATUS_ATTENDED_KEY,\
    EVENT_INVITATION_ATTEND_STATUS_UNCHECKED_KEY, EVENT_INVITATION_ATTEND_STATUS_MISSED_KEY
from models.User import User, PredefinedPoints

from utils.errors import UserAlreadyExists, UserLoginFailed
from validators.UserValidator import UserValidator


class UserService:
    def __init__(self, validator: UserValidator):
        self.validator = validator

    def add(self, username: str, password: str, first_name: str, last_name: str) -> User:
        self.validator.validate_parameters(username, password, first_name, last_name)

        try:
            User.objects.get(username__exact=username)
            raise UserAlreadyExists(username)
        except DoesNotExist:
            pass

        user = User(username=username, first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save()

        return user

    def add_points(self, user: User, points: int = 0, old_invitation_attend_status: int = None,
                   new_invitation_attend_status: int = None):
        invitation_attend_transition_points = [
            (EVENT_INVITATION_ATTEND_STATUS_UNCHECKED_KEY, EVENT_INVITATION_ATTEND_STATUS_ATTENDED_KEY,
             PredefinedPoints.ATTEND_EVENT.value * 1),
            (EVENT_INVITATION_ATTEND_STATUS_ATTENDED_KEY, EVENT_INVITATION_ATTEND_STATUS_UNCHECKED_KEY,
             PredefinedPoints.ATTEND_EVENT.value * -1),

            (EVENT_INVITATION_ATTEND_STATUS_MISSED_KEY, EVENT_INVITATION_ATTEND_STATUS_UNCHECKED_KEY,
             PredefinedPoints.ATTEND_EVENT.value * 1),
            (EVENT_INVITATION_ATTEND_STATUS_UNCHECKED_KEY, EVENT_INVITATION_ATTEND_STATUS_MISSED_KEY,
             PredefinedPoints.ATTEND_EVENT.value * -1),

            (EVENT_INVITATION_ATTEND_STATUS_ATTENDED_KEY, EVENT_INVITATION_ATTEND_STATUS_MISSED_KEY,
             PredefinedPoints.ATTEND_EVENT.value * -2),
            (EVENT_INVITATION_ATTEND_STATUS_MISSED_KEY, EVENT_INVITATION_ATTEND_STATUS_ATTENDED_KEY,
             PredefinedPoints.ATTEND_EVENT.value * 2),
        ]

        if old_invitation_attend_status is not None and new_invitation_attend_status is not None:
            for from_key, to_key, change in invitation_attend_transition_points:
                if old_invitation_attend_status == from_key and new_invitation_attend_status == to_key:
                    points += change

        User.objects(id=user.id).update_one(inc__points=points)
        user.reload()

    def verify_password(self, user: User, password: str):
        if not user.is_correct_password(password):
            raise UserLoginFailed()

    def find_one_by(self, username: str) -> Union[User, None]:
        try:
            return User.objects.get(username__exact=username)
        except DoesNotExist:
            return None
