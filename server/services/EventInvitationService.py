from typing import Union

from mongoengine import DoesNotExist

from models.Event import Event, event_visibility_map, EVENT_VISIBILITY_WHITELIST, EVENT_VISIBILITY_PUBLIC
from models.EventInvitation import EVENT_INVITATION_STATUS_PENDING, EVENT_INVITATION_STATUS_ACCEPTED, \
    EventInvitation, event_invitation_status_map

from models.User import User
from utils.errors import EventInvitationAlreadyExists, EventInvitationCannotJoinPrivate


class EventInvitationService:
    def join(self, event: Event, user: User):
        try:
            EventInvitation.objects.get(user=user, event=event)
            raise EventInvitationAlreadyExists()
        except DoesNotExist:
            pass

        event_invitation = EventInvitation(event=event, user=user)
        event_invitation.save()

        if event.visibility == event_visibility_map.to_key(EVENT_VISIBILITY_PUBLIC):
            self.accept(event_invitation)

        return event_invitation

    def accept(self, event_invitation: EventInvitation):
        event_invitation.status = event_invitation_status_map.to_key(EVENT_INVITATION_STATUS_ACCEPTED)
        event_invitation.save()

        event_invitation.event.no_participants += 1
        event_invitation.event.save()

    def find_one_by(self, *args, **kwargs) -> Union[EventInvitation, None]:
        try:
            return EventInvitation.objects.get(*args, **kwargs)
        except DoesNotExist:
            return None

    def find_by(self, *args, **kwargs):
        return EventInvitation.objects(*args, **kwargs)

    def find_visible_for_user(self, user: User, event: Event):
        if event.owner.id == user.id:
            return self.find_by()
        else:
            return self.find_by(status=event_invitation_status_map.to_key(EVENT_INVITATION_STATUS_ACCEPTED))

    def find_accepted_user_invitations_event_ids(self, user: User):
        accepted_event_invitations = self.find_by(
            user=user,
            status=event_invitation_status_map.to_key(EVENT_INVITATION_STATUS_ACCEPTED)
        )
        return [ei.id for ei in accepted_event_invitations]
