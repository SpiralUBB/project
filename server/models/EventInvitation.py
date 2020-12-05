from mongoengine import Document, ReferenceField, IntField

from utils.DualMap import DualMap

#
# WARNING
# Do not modify the indices of the following dicts
#

EVENT_INVITATION_STATUS_PENDING_KEY = 0
EVENT_INVITATION_STATUS_ACCEPTED_KEY = 1
EVENT_INVITATION_STATUS_DENIED_KEY = 2

event_invitation_status_map = DualMap({
    EVENT_INVITATION_STATUS_PENDING_KEY: 'pending',
    EVENT_INVITATION_STATUS_ACCEPTED_KEY: 'accepted',
    EVENT_INVITATION_STATUS_DENIED_KEY: 'denied',
}, (-1, 'unknown-status'))

EVENT_INVITATION_ATTEND_STATUS_UNCHECKED_KEY = 0
EVENT_INVITATION_ATTEND_STATUS_ATTENDED_KEY = 1
EVENT_INVITATION_ATTEND_STATUS_MISSED_KEY = 2

event_invitation_attend_status_map = DualMap({
    EVENT_INVITATION_ATTEND_STATUS_UNCHECKED_KEY: 'unchecked',
    EVENT_INVITATION_ATTEND_STATUS_ATTENDED_KEY: 'attended',
    EVENT_INVITATION_ATTEND_STATUS_MISSED_KEY: 'missed',
}, (-1, 'unknown-attend-status'))


class EventInvitation(Document):
    user = ReferenceField('User', required=True)
    event = ReferenceField('Event', required=True)
    status = IntField(min_value=event_invitation_status_map.minimum_key(),
                      max_value=event_invitation_status_map.maximum_key(), required=True)
    attend_status = IntField(min_value=event_invitation_attend_status_map.minimum_key(),
                             max_value=event_invitation_attend_status_map.maximum_key(), required=True)

    meta = {
        'indexes': [
            {
                'fields': [
                    'user',
                    'event',
                ],
                'unique': True,
            },
        ],
    }

    def to_dict(self, with_user: bool = False, with_event: bool = False):
        d = {
            'id': str(self.id),
            'status': self.status,
            'status_text': event_invitation_status_map.to_value(self.status),
            'attend_status': self.attend_status,
            'attend_status_text': event_invitation_attend_status_map.to_value(self.attend_status),
        }

        if with_user:
            d['user'] = self.user.to_dict()

        if with_event:
            d['event'] = self.event.to_dict()

        return d
