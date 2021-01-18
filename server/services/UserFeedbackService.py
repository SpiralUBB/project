from enum import Enum
from typing import Union

from mongoengine import DoesNotExist, NotUniqueError
from pyee import BaseEventEmitter

from models.Event import Event
from models.UserFeedback import UserFeedback
from models.User import User
from utils.errors import UserFeedbackAlreadyExists
from validators.UserFeedbackValidator import UserFeedbackValidator


class UserFeedbackServiceEvents(Enum):
    FEEDBACK_POINTS_UPDATED = 'feedback-points-updated'


class UserFeedbackService:
    def __init__(self, validator: UserFeedbackValidator):
        self.validator = validator
        self.emitter = BaseEventEmitter()

    def add(self, from_user: User, to_user: User, event: Event, points: int, message: Union[str, None] = None):
        points = self.validator.parse_points(points)

        user_feedback = UserFeedback(event=event, from_user=from_user, to_user=to_user, points=points, message=message)
        try:
            user_feedback.save()
        except NotUniqueError:
            raise UserFeedbackAlreadyExists()

        self.emitter.emit(UserFeedbackServiceEvents.FEEDBACK_POINTS_UPDATED, to_user, 0, points)

        return user_feedback

    def update(self, user_feedback: UserFeedback, points: int = None, message: str = None):
        old_points = user_feedback.points

        if points is not None:
            points = self.validator.parse_points(points)
            user_feedback.points = points

        if message is not None:
            user_feedback.message = message

        user_feedback.save()

        self.emitter.emit(UserFeedbackServiceEvents.FEEDBACK_POINTS_UPDATED, user_feedback.to_user, old_points, points)

        return user_feedback

    def find_one_by(self, *args, **kwargs) -> Union[UserFeedback, None]:
        try:
            return UserFeedback.objects.get(*args, **kwargs)
        except DoesNotExist:
            return None
