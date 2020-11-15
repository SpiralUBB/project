from typing import Union

from mongoengine import DoesNotExist

from models.Event import Event
from models.EventInvitation import EVENT_INVITATION_STATUS_PENDING, EVENT_INVITATION_STATUS_ACCEPTED, \
    EventInvitation, event_invitation_status_map

from models.User import User


class EventInvitationService:
    def add(self, event: Event, user: User,
            accepted: bool = False):
        status = event_invitation_status_map.to_key(EVENT_INVITATION_STATUS_ACCEPTED) if accepted \
            else event_invitation_status_map.to_key(EVENT_INVITATION_STATUS_PENDING)
        event_invitation = EventInvitation(event=event, user=user, status=status)
        event_invitation.save()
        return event_invitation

    def accept(self, event_invitation: EventInvitation):
        event_invitation.status = event_invitation_status_map.to_key(EVENT_INVITATION_STATUS_ACCEPTED)
        event_invitation.save()

    def find_one_by(self, *args, **kwargs) -> Union[EventInvitation, None]:
        try:
            return EventInvitation.objects.get(*args, **kwargs)
        except DoesNotExist:
            return None

    def find_by(self, *args, **kwargs):
        return EventInvitation.objects(*args, **kwargs)

    def find_accepted_user_invitations_event_ids(self, user: User):
        accepted_event_invitations = self.find_by(
            user=user,
            status=event_invitation_status_map.to_key(EVENT_INVITATION_STATUS_ACCEPTED)
        )
        return [ei.id for ei in accepted_event_invitations]
