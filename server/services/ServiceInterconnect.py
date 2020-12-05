from models.Event import EVENT_VISIBILITY_PUBLIC_KEY
from models.EventInvitation import EventInvitation, EVENT_INVITATION_STATUS_ACCEPTED_KEY, EventInvitationData, \
    EVENT_INVITATION_ATTEND_STATUS_ATTENDED_KEY
from models.User import PredefinedPoints
from services.EventInvitationService import EventInvitationService
from services.EventService import EventService
from services.UserService import UserService


class ServiceInterconnect:
    def __init__(self, user_service: UserService, event_service: EventService,
                 event_invitation_service: EventInvitationService):
        self.user_service = user_service
        self.event_service = event_service
        self.event_invitation_service = event_invitation_service

    def on_event_added(self, event):
        self.event_invitation_service.add(event, event.owner,
                                          status=EVENT_INVITATION_STATUS_ACCEPTED_KEY,
                                          attend_status=EVENT_INVITATION_ATTEND_STATUS_ATTENDED_KEY)

        self.user_service.add_points(event.owner, PredefinedPoints.CREATE_EVENT.value)

    def on_event_deleted(self, event):
        self.user_service.add_points(event.owner, -PredefinedPoints.CREATE_EVENT.value)

    def on_event_invitation_added(self, event_invitation: EventInvitation):
        if event_invitation.event.visibility == EVENT_VISIBILITY_PUBLIC_KEY:
            self.event_invitation_service.update(event_invitation, status=EVENT_INVITATION_STATUS_ACCEPTED_KEY)

        self.user_service.add_points(event_invitation.event.owner, PredefinedPoints.JOIN_EVENT_FOR_OWNER.value)

    def on_event_invitation_updated(self, event_invitation: EventInvitation, old_invitation_data: EventInvitationData):
        self.event_service.add_participants(event_invitation.event,
                                            old_invitation_status=old_invitation_data.status,
                                            new_invitation_status=event_invitation.status)

        self.user_service.add_points(event_invitation.user,
                                     old_invitation_attend_status=old_invitation_data.attend_status,
                                     new_invitation_attend_status=event_invitation.attend_status)
