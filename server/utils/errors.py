class HttpError(Exception):
    def __init__(self, message, code, status, *args, original_message=None, **kwargs):
        super().__init__(message)

        self.code = code
        self.status = status
        self.message = message
        self.original_message = original_message

    def to_dict(self):
        return {
            'code': self.code,
            'message': self.message,
            'original_message': self.original_message,
            'error': True,
        }


def make_error(base_class, name, code, status, default_message, **default_kwargs):
    def __init__(self, message=default_message, **kwargs):
        merged_kwargs = {}
        merged_kwargs.update(default_kwargs)
        merged_kwargs.update(kwargs)
        base_class.__init__(self, message, code, status, **merged_kwargs)

    return type(name, (base_class,), {
        '__init__': __init__,
    })


def make_http_error(name, code, status, message, **kwargs):
    return make_error(HttpError, name, code, status, message, **kwargs)


UserAlreadyExists = make_http_error('UserAlreadyExists',
                                    'user-already-exists', 403,
                                    'User already exists')
UserDoesNotExist = make_http_error('UserDoesNotExist',
                                   'user-not-exist', 404,
                                   'User does not exist')
UserUsernameInvalid = make_http_error('UserUsernameInvalid',
                                      'user-username-invalid', 400,
                                      'User username is invalid')
UserPasswordInvalid = make_http_error('UserPasswordInvalid',
                                      'user-password-invalid', 400,
                                      'User password is invalid')
UserFirstNameInvalid = make_http_error('UserFirstNameInvalid',
                                       'user-first-name-invalid', 400,
                                       'User first name is invalid')
UserLastNameInvalid = make_http_error('UserLastNameInvalid',
                                      'user-last-name-invalid', 400,
                                      'User last name is invalid')
UserLoginFailed = make_http_error('UserLoginFailed',
                                  'user-login-failed', 401,
                                  'User login failed')
UserNotLoggedIn = make_http_error('UserNotLoggedIn',
                                  'user-not-logged-in', 401,
                                  'User not logged in')
UserLoggedInInvalid = make_http_error('UserLoggedInInvalid',
                                      'user-logged-in-invalid', 401,
                                      'User logged in is invalid')
UserTokenExpired = make_http_error('UserTokenExpired',
                                   'user-token-expired', 401,
                                   'User token expired')
UserTokenInvalid = make_http_error('UserTokenInvalid',
                                   'user-token-invalid', 422,
                                   'User token is invalid')
EventDoesNotExist = make_http_error('EventDoesNotExist',
                                    'event-not-exist', 404,
                                    'Event does not exist')
EventOwnerInvalid = make_http_error('EventOwnerInvalid',
                                    'event-owner-invalid', 400,
                                    'Event owner is invalid')
EventTitleInvalid = make_http_error('EventTitleInvalid',
                                    'event-title-invalid', 400,
                                    'Event title is invalid')
EventLocationInvalid = make_http_error('EventLocationInvalid',
                                       'event-location-invalid', 400,
                                       'Event location is invalid')
EventLocationPointInvalid = make_http_error('EventLocationPointInvalid',
                                            'event-location-point-invalid', 400,
                                            'Event location point is invalid')
EventTimeInvalid = make_http_error('EventTimeInvalid',
                                   'event-time-invalid', 400,
                                   'Event time is invalid')
EventMaxNoParticipantsInvalid = make_http_error('EventMaxNoParticipantsInvalid',
                                                'event-max-no-participants-invalid', 400,
                                                'Event max number of participants is invalid')
EventMinTrustLevelInvalid = make_http_error('EventMinTrustLevelInvalid',
                                            'event-min-trust-level-invalid', 400,
                                            'Event min trust level invalid')
EventDescriptionInvalid = make_http_error('EventDescriptionInvalid',
                                          'event-description-invalid', 400,
                                          'Event description is invalid')
EventVisibilityInvalid = make_http_error('EventVisibilityInvalid',
                                         'event-visibility-invalid', 400,
                                         'Event visibility type is invalid')
EventCategoryInvalid = make_http_error('EventCategoryInvalid',
                                       'event-category-invalid', 400,
                                       'Event category is invalid')
EventCommentDoesNotExist = make_http_error('EventCommentDoesNotExist',
                                           'event-comment-not-exist', 404,
                                           'Event comment does not exist')
EventCommentAuthorInvalid = make_http_error('EventCommentAuthorInvalid',
                                            'event-comment-author-invalid', 400,
                                            'Event comment author invalid')
EventInvitationAlreadyExists = make_http_error('EventInvitationAlreadyExists',
                                               'event-invitation-already-exists', 403,
                                               'Event invitation already exists')
EventInvitationDoesNotExist = make_http_error('EventInvitationDoesNotExist',
                                              'event-invitation-not-exist', 404,
                                              'Event invitation does not exist')
EventInvitationStatusInvalid = make_http_error('EventInvitationStatusInvalid',
                                               'event-invitation-status-invalid', 400,
                                               'Event invitation status is invalid')
EventInvitationAttendStatusInvalid = make_http_error('EventInvitationAttendStatusInvalid',
                                                     'event-invitation-attend-status-invalid', 400,
                                                     'Event invitation attend status is invalid')
EventInvitationCannotJoinOwn = make_http_error('EventInvitationCannotJoinOwn',
                                               'event-invitation-cannot-join-own', 400,
                                               'Cannot join an event owned by yourself')
EventInvitationCannotJoinFull = make_http_error('EventInvitationCannotJoinFull',
                                                'event-invitation-cannot-join-full', 400,
                                                'Cannot join a full event')
EventInvitationCannotModifyOwner = make_http_error('EventInvitationCannotModifyOwner',
                                                   'event-invitation-cannot-modify owner', 400,
                                                   "Cannot modify event owner invitation")
EventCommentEventInvalid = make_http_error('EventCommentEventInvalid',
                                           'event-comment-event-invalid', 400,
                                           'Event comment event invalid')
EventCommentTextInvalid = make_http_error('EventCommentTextInvalid',
                                          'event-comment-text-invalid', 400,
                                          'Event comment text invalid')
UserFeedbackAlreadyExists = make_http_error('UserFeedbackAlreadyExists',
                                            'user-feedback-already-exists', 400,
                                            'User feedback already exists')
UserFeedbackDoesNotExist = make_http_error('UserFeedbackDoesNotExist',
                                           'user-feedback-not-exist', 400,
                                           'User feedback does not exist')
UserFeedbackPointsInvalid = make_http_error('UserFeedbackPointsInvalid',
                                            'user-feedback-points-invalid', 400,
                                            'User feedback points invalid')
UserFeedbackCannotGiveOwn = make_http_error('UserFeedbackCannotGiveOwn',
                                            'user-feedback-cannot-give-own', 400,
                                            'Cannot give user feedback to yourself')
PaginationLimitInvalid = make_http_error('PaginationLimitInvalid',
                                         'pagination-limit-invalid', 400,
                                         'Pagination limit invalid')
PaginationPageInvalid = make_http_error('PaginationPageInvalid',
                                        'pagination-page-invalid', 400,
                                        'Pagination page invalid')
