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
            'error': True,
        }


class UserAlreadyExists(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'User already exists'

        super().__init__(message, 'user-already-exists', 403)


class UserDoesNotExist(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'User does not exist'

        super().__init__(message, 'user-not-exist', 404)


class UserUsernameInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'User username is invalid'

        super().__init__(message, 'user-username-invalid', 400)


class UserPasswordInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'User password is invalid'

        super().__init__(message, 'user-password-invalid', 400)


class UserFirstNameInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'User first name is invalid'

        super().__init__(message, 'user-first-name-invalid', 400)


class UserLastNameInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'User last name is invalid'

        super().__init__(message, 'user-last-name-invalid', 400)


class UserLoginFailed(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'User login failed'

        super().__init__(message, 'user-login-failed', 401)


class UserTokenExpired(HttpError):
    def __init__(self, token=None):
        if token:
            message = 'User {} token expired'
        else:
            message = 'User token expired'

        super().__init__(message, 'user-token-expired', 401)


class UserTokenInvalid(HttpError):
    def __init__(self, reason=None):
        message = 'User token is invalid: {}'.format(reason)
        super().__init__(message, 'user-token-invalid', 422)


class EventAlreadyExists(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Event already exists'

        super().__init__(message, 'event-already-exists', 403)


class EventDoesNotExist(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Event does not exist'

        super().__init__(message, 'event-not-exist', 404)


class EventOwnerInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Event owner is invalid'

        super().__init__(message, 'event-owner-invalid', 400)


class EventTitleInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Event title is invalid'

        super().__init__(message, 'event-title-invalid', 400)


class EventLocationInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Event location is invalid'

        super().__init__(message, 'event-location-invalid', 400)


class EventLocationPointInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Event location point is invalid'

        super().__init__(message, 'event-location-point-invalid', 400)


class EventDateInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Event date is invalid'

        super().__init__(message, 'event-date-invalid', 400)


class EventDescriptionInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Event description is invalid'

        super().__init__(message, 'event-description-invalid', 400)


class EventVisibilityInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Event visibility type is invalid'

        super().__init__(message, 'event-visibility-invalid', 400)


class EventCategoryInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Event category is invalid'

        super().__init__(message, 'event-category-invalid', 400)


class EventCommentDoesNotExist(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Event comment does not exist'

        super().__init__(message, 'event-comment-not-exist', 404)


class EventCommentAuthorInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Event comment author invalid'

        super().__init__(message, 'event-comment-author-invalid', 400)


class EventCommentEventInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Event comment event invalid'

        super().__init__(message, 'event-comment-event-invalid', 400)


class EventCommentTextInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Event comment text invalid'

        super().__init__(message, 'event-comment-text-invalid', 400)


class PaginationLimitInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Pagination limit invalid'

        super().__init__(message, 'pagination-limit-invalid', 400)


class PaginationPageInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Pagination page invalid'

        super().__init__(message, 'pagination-page-invalid', 400)
