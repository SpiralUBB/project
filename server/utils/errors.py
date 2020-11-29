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
            message = 'User {} token expired'.format(token)
        else:
            message = 'User token expired'

        super().__init__(message, 'user-token-expired', 401)


class UserTokenInvalid(HttpError):
    def __init__(self, reason=None):
        message = 'User token is invalid: {}'.format(reason)
        super().__init__(message, 'user-token-invalid', 422)


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


class EventTimeInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Event time is invalid'

        super().__init__(message, 'event-time-invalid', 400)


class EventMaxNoParticipantsInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Event max number of participants is invalid'

        super().__init__(message, 'event-max-no-participants-invalid', 400)


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


class EventInvitationAlreadyExists(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Event invitation already exists'

        super().__init__(message, 'event-invitation-already-exists', 403)


class EventInvitationDoesNotExist(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Event invitation does not exist'

        super().__init__(message, 'event-invitation-not-exist', 404)


class EventInvitationStatusInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Event invitation status is invalid'

        super().__init__(message, 'event-invitation-status-invalid', 400)


class EventInvitationAttendStatusInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Event invitation attend status is invalid'

        super().__init__(message, 'event-invitation-attend-status-invalid', 400)


class EventInvitationCannotJoinOwn(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Cannot join an event owned by yourself'

        super().__init__(message, 'event-invitation-cannot-join-own', 400)


class EventInvitationCannotJoinFull(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Cannot join a full event'

        super().__init__(message, 'event-invitation-cannot-join-full', 400)


class EventInvitationCannotModifyOwn(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Cannot modify invitation for own event'

        super().__init__(message, 'event-invitation-cannot-modify own', 400)

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


class UserFeedbackAlreadyExists(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'User feedback already exists'

        super().__init__(message, 'user-feedback-already-exists', 400)


class UserFeedbackDoesNotExist(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'User feedback does not exist'

        super().__init__(message, 'user-feedback-not-exist', 400)


class UserFeedbackPointsInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'User feedback points invalid'

        super().__init__(message, 'user-feedback-points-invalid', 400)


class UserFeedbackCannotGiveOwn(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Cannot give user feedback to yourself'

        super().__init__(message, 'user-feedback-cannot-give-own', 400)


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
