class HttpError(Exception):
    def __init__(self, message, code, status):
        super().__init__(message)

        self.code = code
        self.status = status
        self.message = message

    def to_dict(self):
        return {
            'code': self.code,
            'message': self.message,
        }


"""
    User error messages
"""


class UserAlreadyExistsError(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'User already exists'

        super().__init__(message, 'user-already-exists', 403)


class UserDoesNotExist(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'User does not exist'

        super().__init__(message, 'user-not-exist', 404)


class UsernameInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Username is invalid'

        super().__init__(message, 'username-invalid', 400)


class PasswordInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Password is invalid'

        super().__init__(message, 'password-invalid', 400)


class FirstNameInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'First name is invalid'

        super().__init__(message, 'first-name-invalid', 400)


class LastNameInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Last name is invalid'

        super().__init__(message, 'last-name-invalid', 400)


class LoginFailed(HttpError):
    def __init__(self):
        super().__init__('Login failed', 'login-failed', 401)


"""
    Event error messages
"""


class EventAlreadyExistsError(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Event already exists'

        super().__init__(message, 'event-already-exists', 403)


class EventDoesNotExist(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Event does not exist'

        super().__init__(message, 'event-not-exist', 404)


class IdInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'ID is invalid'

        super().__init__(message, 'id-invalid', 400)


class UsernameInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Username of the creator is invalid'

        super().__init__(message, 'id-creator-invalid', 400)


class TitleInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Title is invalid'

        super().__init__(message, 'title-invalid', 400)


class LocationInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Location is invalid'

        super().__init__(message, 'location-invalid', 400)


class DateInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Date is invalid'

        super().__init__(message, 'date-invalid', 400)


class DescriptionInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Description is invalid'

        super().__init__(message, 'description-invalid', 400)


class PrivacyInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Privacy type is invalid'

        super().__init__(message, 'privacy-invalid', 400)


class TypeInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Event type is invalid'

        super().__init__(message, 'type-invalid', 400)


class AddEventFailed(HttpError):
    def __init__(self):
        super().__init__('Adding the event failed', 'add-event-failed', 401)


class DeleteEventFailed(HttpError):
    def __init__(self):
        super().__init__('Deleting the event failed', 'delete-event-failed', 401)


class ReadEventFailed(HttpError):
    def __init__(self):
        super().__init__('Loading the event failed', 'read-event-failed', 401)


class UpdateEventFailed(HttpError):
    def __init__(self):
        super().__init__('Updating the event failed', 'update-event-failed', 401)
