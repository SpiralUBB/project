from typing import Union

from mongoengine import DoesNotExist, Q, NotUniqueError

from models.Event import Event
from models.EventInvitation import EventInvitation, EVENT_INVITATION_STATUS_PENDING_KEY, \
    EVENT_INVITATION_STATUS_ACCEPTED_KEY, EVENT_INVITATION_ATTEND_STATUS_UNCHECKED_KEY

from models.User import User
from utils.errors import EventInvitationAlreadyExists
from validators.EventInvitationValidator import EventInvitationValidator


class EventInvitationService:
    def __init__(self, validator: EventInvitationValidator):
        self.validator = validator

    def add(self, event: Event, user: User, status: Union[str, int] = EVENT_INVITATION_STATUS_PENDING_KEY,
            attend_status: Union[str, int] = EVENT_INVITATION_ATTEND_STATUS_UNCHECKED_KEY):
        status = self.validator.parse_status(status)

        event_invitation = EventInvitation(event=event, user=user, status=status, attend_status=attend_status)
        try:
            event_invitation.save()
        except NotUniqueError:
            raise EventInvitationAlreadyExists()

        return event_invitation

    def update(self, event_invitation: EventInvitation, status: Union[str, int] = None,
               attend_status: Union[str, int] = None):
        if status is not None:
            status = self.validator.parse_status(status)
            event_invitation.status = status

        if attend_status is not None:
            attend_status = self.validator.parse_attend_status(attend_status)
            event_invitation.attend_status = attend_status

        event_invitation.save()

    def find_one_by(self, *args, **kwargs) -> Union[EventInvitation, None]:
        try:
            return EventInvitation.objects.get(*args, **kwargs)
        except DoesNotExist:
            return None

    def find_by(self, *args, **kwargs):
        return EventInvitation.objects(*args, **kwargs)

    def find_visible_for_user(self, user: User, event: Event):
        query = Q(event=event)

        if event.owner.id != user.id:
            query &= Q(status=EVENT_INVITATION_STATUS_ACCEPTED_KEY)

        return self.find_by(query)

    def find_accepted_user_invitations_event_ids(self, user: User):
        if user is None:
            accepted_event_invitations = []
        else:
            accepted_event_invitations = self.find_by(
                user=user,
                status=EVENT_INVITATION_STATUS_ACCEPTED_KEY
            )

        return [ei.id for ei in accepted_event_invitations]
