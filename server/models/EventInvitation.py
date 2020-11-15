from mongoengine import Document, ReferenceField, IntField

from utils.DualMap import DualMap

EVENT_INVITATION_STATUS_PENDING = 'pending'
EVENT_INVITATION_STATUS_ACCEPTED = 'accepted'

event_invitation_status_map = DualMap({
    0: EVENT_INVITATION_STATUS_PENDING,
    1: EVENT_INVITATION_STATUS_ACCEPTED,
}, (-1, 'unknown'))


class EventInvitation(Document):
    user = ReferenceField('User', required=True)
    event = ReferenceField('Event', required=True)
    status = IntField(min_value=event_invitation_status_map.minimum_key(),
                      max_value=event_invitation_status_map.maximum_key(), required=True)

    def to_dict(self, with_user: bool = False, with_event: bool = False):
        d = {
            'id': str(self.id),
            'status': event_invitation_status_map.to_value(self.status),
        }

        if with_user:
            d['user'] = self.user.to_dict()

        if with_event:
            d['event'] = self.event.to_dict()

        return d
