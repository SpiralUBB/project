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


def HttpErrorFactory(name, code, status, default_message):
    def __init__(self, message=default_message):
        HttpError.__init__(self, message, code, status)

    return type(name, (HttpError, ), {
        '__init__': __init__,
    })


UserAlreadyExists = HttpErrorFactory('UserAlreadyExists', 'user-already-exists', 403,
                                     'User already exists')
UserDoesNotExist = HttpErrorFactory('UserDoesNotExist', 'user-not-exist', 404,
                                    'User does not exist')
UserUsernameInvalid = HttpErrorFactory('UserUsernameInvalid', 'user-username-invalid', 400,
                                       'User username is invalid')
UserPasswordInvalid = HttpErrorFactory('UserPasswordInvalid', 'user-password-invalid', 400,
                                       'User password is invalid')
UserFirstNameInvalid = HttpErrorFactory('UserFirstNameInvalid', 'user-first-name-invalid', 400,
                                        'User first name is invalid')
UserLastNameInvalid = HttpErrorFactory('UserLastNameInvalid', 'user-last-name-invalid', 400,
                                       'User last name is invalid')
UserLoginFailed = HttpErrorFactory('UserLoginFailed', 'user-login-failed', 401,
                                   'User login failed')
UserTokenExpired = HttpErrorFactory('UserTokenExpired', 'user-token-expired', 401,
                                    'User token expired')
UserTokenInvalid = HttpErrorFactory('UserTokenInvalid', 'user-token-invalid', 422,
                                    'User token is invalid')
EventDoesNotExist = HttpErrorFactory('EventDoesNotExist', 'event-not-exist', 404,
                                     'Event does not exist')
EventOwnerInvalid = HttpErrorFactory('EventOwnerInvalid', 'event-owner-invalid', 400,
                                     'Event owner is invalid')
EventTitleInvalid = HttpErrorFactory('EventTitleInvalid', 'event-title-invalid', 400,
                                     'Event title is invalid')
EventLocationInvalid = HttpErrorFactory('EventLocationInvalid', 'event-location-invalid', 400,
                                        'Event location is invalid')
EventLocationPointInvalid = HttpErrorFactory('EventLocationPointInvalid', 'event-location-point-invalid', 400,
                                             'Event location point is invalid')
EventTimeInvalid = HttpErrorFactory('EventTimeInvalid', 'event-time-invalid', 400,
                                    'Event time is invalid')
EventMaxNoParticipantsInvalid = HttpErrorFactory('EventMaxNoParticipantsInvalid',
                                                 'event-max-no-participants-invalid', 400,
                                                 'Event max number of participants is invalid')
EventDescriptionInvalid = HttpErrorFactory('EventDescriptionInvalid', 'event-description-invalid', 400,
                                           'Event description is invalid')
EventVisibilityInvalid = HttpErrorFactory('EventVisibilityInvalid', 'event-visibility-invalid', 400,
                                          'Event visibility type is invalid')
EventCategoryInvalid = HttpErrorFactory('EventCategoryInvalid', 'event-category-invalid', 400,
                                        'Event category is invalid')
EventCommentDoesNotExist = HttpErrorFactory('EventCommentDoesNotExist', 'event-comment-not-exist', 404,
                                            'Event comment does not exist')
EventCommentAuthorInvalid = HttpErrorFactory('EventCommentAuthorInvalid', 'event-comment-author-invalid', 400,
                                             'Event comment author invalid')
EventInvitationAlreadyExists = HttpErrorFactory('EventInvitationAlreadyExists', 'event-invitation-already-exists', 403,
                                                'Event invitation already exists')
EventInvitationDoesNotExist = HttpErrorFactory('EventInvitationDoesNotExist', 'event-invitation-not-exist', 404,
                                               'Event invitation does not exist')
EventInvitationStatusInvalid = HttpErrorFactory('EventInvitationStatusInvalid', 'event-invitation-status-invalid', 400,
                                                'Event invitation status is invalid')
EventInvitationAttendStatusInvalid = HttpErrorFactory('EventInvitationAttendStatusInvalid',
                                                      'event-invitation-attend-status-invalid', 400,
                                                      'Event invitation attend status is invalid')
EventInvitationCannotJoinOwn = HttpErrorFactory('EventInvitationCannotJoinOwn', 'event-invitation-cannot-join-own', 400,
                                                'Cannot join an event owned by yourself')
EventInvitationCannotJoinFull = HttpErrorFactory('EventInvitationCannotJoinFull',
                                                 'event-invitation-cannot-join-full', 400,
                                                 'Cannot join a full event')
EventInvitationCannotModifyOwn = HttpErrorFactory('EventInvitationCannotModifyOwn',
                                                  'event-invitation-cannot-modify own', 400,
                                                  'Cannot modify invitation for own event')
EventCommentEventInvalid = HttpErrorFactory('EventCommentEventInvalid', 'event-comment-event-invalid', 400,
                                            'Event comment event invalid')
EventCommentTextInvalid = HttpErrorFactory('EventCommentTextInvalid', 'event-comment-text-invalid', 400,
                                           'Event comment text invalid')
UserFeedbackAlreadyExists = HttpErrorFactory('UserFeedbackAlreadyExists', 'user-feedback-already-exists', 400,
                                             'User feedback already exists')
UserFeedbackDoesNotExist = HttpErrorFactory('UserFeedbackDoesNotExist', 'user-feedback-not-exist', 400,
                                            'User feedback does not exist')
UserFeedbackPointsInvalid = HttpErrorFactory('UserFeedbackPointsInvalid', 'user-feedback-points-invalid', 400,
                                             'User feedback points invalid')
UserFeedbackCannotGiveOwn = HttpErrorFactory('UserFeedbackCannotGiveOwn', 'user-feedback-cannot-give-own', 400,
                                             'Cannot give user feedback to yourself')
PaginationLimitInvalid = HttpErrorFactory('PaginationLimitInvalid', 'pagination-limit-invalid', 400,
                                          'Pagination limit invalid')
PaginationPageInvalid = HttpErrorFactory('PaginationPageInvalid', 'pagination-page-invalid', 400,
                                         'Pagination page invalid')
