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

    def to_dict(self):
        return {
            'user': self.user.to_dict(),
            'status': event_invitation_status_map.to_value(self.status),
        }
