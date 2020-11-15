from typing import Union

from mongoengine import DoesNotExist

from models.User import User

from utils.errors import UserAlreadyExists, UserDoesNotExist, UserLoginFailed
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

    def verify_password(self, user: User, password: str):
        if not user.is_correct_password(password):
            raise UserLoginFailed()

    def find_one_by(self, username: str) -> Union[User, None]:
        try:
            return User.objects.get(username__exact=username)
        except DoesNotExist:
            return None
