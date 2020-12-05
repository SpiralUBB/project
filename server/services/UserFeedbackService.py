from typing import Union

from mongoengine import DoesNotExist, NotUniqueError

from models.Event import Event
from models.UserFeedback import UserFeedback
from models.User import User
from utils.errors import UserFeedbackAlreadyExists
from validators.UserFeedbackValidator import UserFeedbackValidator


class UserFeedbackService:
    def __init__(self, validator: UserFeedbackValidator):
        self.validator = validator

    def add(self, from_user: User, to_user: User, event: Event, points: int, message: Union[str, None]):
        points = self.validator.parse_points(points)

        user_feedback = UserFeedback.objects.get(event=event, from_user=from_user, to_user=to_user, points=points,
                                                 message=message)
        try:
            user_feedback.save()
        except NotUniqueError:
            raise UserFeedbackAlreadyExists()

    def update(self, user_feedback: UserFeedback, points: int = None, message: str = None):
        if points is not None:
            points = self.validator.parse_points(points)
            user_feedback.points = points

        if message is not None:
            user_feedback.message = message

        user_feedback.save()

    def find_one_by(self, *args, **kwargs) -> Union[UserFeedback, None]:
        try:
            return UserFeedback.objects.get(*args, **kwargs)
        except DoesNotExist:
            return None
