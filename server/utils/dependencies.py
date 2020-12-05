from flask_injector import request
from injector import Injector

from services.UserService import UserService
from services.UserFeedbackService import UserFeedbackService
from services.EventService import EventService, EventServiceEvents
from services.EventCommentService import EventCommentService
from services.EventInvitationService import EventInvitationService, EventInvitationServiceEvents
from services.ServiceInterconnect import ServiceInterconnect
from validators.EventCommentValidator import EventCommentValidator
from validators.EventInvitationValidator import EventInvitationValidator
from validators.UserFeedbackValidator import UserFeedbackValidator
from validators.UserValidator import UserValidator
from validators.EventValidator import EventValidator


def configure_services(binder):
    user_validator = UserValidator()
    user_service = UserService(user_validator)
    binder.bind(UserService, to=user_service, scope=request)

    event_validator = EventValidator()
    event_service = EventService(event_validator)
    binder.bind(EventService, to=event_service, scope=request)

    event_comment_validator = EventCommentValidator()
    event_comment_service = EventCommentService(event_comment_validator)
    binder.bind(EventCommentService, to=event_comment_service, scope=request)

    event_invitation_validator = EventInvitationValidator()
    event_invitation_service = EventInvitationService(event_invitation_validator)
    binder.bind(EventInvitationService, to=event_invitation_service, scope=request)

    user_feedback_validator = UserFeedbackValidator()
    user_feedback_service = UserFeedbackService(user_feedback_validator)
    binder.bind(UserFeedbackService, to=user_feedback_service, scope=request)

    service_interconnect = ServiceInterconnect(user_service, event_service, event_invitation_service)

    event_service.emitter.on(EventServiceEvents.EVENT_ADDED, service_interconnect.on_event_added)
    event_service.emitter.on(EventServiceEvents.EVENT_DELETED, service_interconnect.on_event_deleted)

    event_invitation_service.emitter.on(EventInvitationServiceEvents.INVITATION_ADDED,
                                        service_interconnect.on_event_invitation_added)
    event_invitation_service.emitter.on(EventInvitationServiceEvents.INVITATION_UPDATED,
                                        service_interconnect.on_event_invitation_updated)


services_injector = Injector([configure_services])
