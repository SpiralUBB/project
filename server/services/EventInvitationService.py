from enum import Enum
from typing import Union, List

from mongoengine import DoesNotExist, Q, NotUniqueError
from pyee import BaseEventEmitter

from models.Event import Event, EVENT_VISIBILITY_PUBLIC_KEY
from models.EventInvitation import EventInvitation, EVENT_INVITATION_STATUS_PENDING_KEY, \
    EVENT_INVITATION_STATUS_ACCEPTED_KEY, EVENT_INVITATION_ATTEND_STATUS_UNCHECKED_KEY

from models.User import User
from utils.errors import EventInvitationAlreadyExists, EventInvitationCannotJoinFull, EventInvitationCannotModifyOwner
from validators.EventInvitationValidator import EventInvitationValidator


class EventInvitationServiceEvents(Enum):
    INVITATION_ADDED = 'invitation-added'
    INVITATION_UPDATED = 'invitation-updated'


class EventInvitationService:
    def __init__(self, validator: EventInvitationValidator):
        self.validator = validator
        self.emitter = BaseEventEmitter()

    def add(self, event: Event, user: User, status: Union[str, int] = EVENT_INVITATION_STATUS_PENDING_KEY,
            attend_status: Union[str, int] = EVENT_INVITATION_ATTEND_STATUS_UNCHECKED_KEY):
        status = self.validator.parse_status(status)

        if not event.allows_more_participants():
            raise EventInvitationCannotJoinFull()

        if event.visibility == EVENT_VISIBILITY_PUBLIC_KEY:
            status = EVENT_INVITATION_STATUS_ACCEPTED_KEY

        event_invitation = EventInvitation(event=event, user=user, status=status, attend_status=attend_status)
        try:
            event_invitation.save()
        except NotUniqueError:
            raise EventInvitationAlreadyExists()

        self.emitter.emit(EventInvitationServiceEvents.INVITATION_ADDED, event_invitation)

        return event_invitation

    def update(self, event_invitation: EventInvitation, status: Union[str, int] = None,
               attend_status: Union[str, int] = None):
        if event_invitation.user.id == event_invitation.event.owner.id:
            raise EventInvitationCannotModifyOwner()

        old_data = event_invitation.to_data()

        if status is not None:
            status = self.validator.parse_status(status)
            event_invitation.status = status

        if attend_status is not None:
            attend_status = self.validator.parse_attend_status(attend_status)
            event_invitation.attend_status = attend_status

        event_invitation.save()

        self.emitter.emit(EventInvitationServiceEvents.INVITATION_UPDATED, event_invitation, old_data)

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

    def find_for_user_status_event_ids(self, user: User = None, statuses: List[Union[str, int]] = None):
        if user is None:
            return []

        if not statuses:
            return []

        statuses = [self.validator.parse_status(s) for s in statuses]

        event_invitations = self.find_by(
            user=user,
            status__in=statuses,
        )

        return [ei.id for ei in event_invitations]

    def find_accepted_user_invitations_event_ids(self, user: User = None):
        return self.find_for_user_status_event_ids(user, [EVENT_INVITATION_STATUS_ACCEPTED_KEY])
