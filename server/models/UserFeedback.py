from mongoengine import Document, ReferenceField, IntField, StringField, CASCADE


class UserFeedback(Document):
    from_user = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    to_user = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    event = ReferenceField('Event', reverse_delete_rule=CASCADE)
    message = StringField()
    points = IntField(required=True)

    meta = {
        'indexes': [
            {
                'fields': [
                    'event',
                    'from_user',
                    'to_user',
                ],
                'unique': True,
            },
        ],
    }

    def to_dict(self, with_event=False, with_from_user=False, with_to_user=False, with_event_details=False):
        d = {
            'points': self.points,
            'message': self.message,
        }

        if with_event and self.event:
            d['event'] = self.event.to_dict(with_details=with_event_details)

        if with_from_user:
            d['from_user'] = self.from_user.to_dict()

        if with_to_user:
            d['to_user'] = self.to_user.to_dict()

        return d
