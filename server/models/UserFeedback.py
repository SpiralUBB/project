from mongoengine import Document, ReferenceField, IntField, StringField


class UserFeedback(Document):
    from_user = ReferenceField('User', required=True)
    to_user = ReferenceField('User', required=True)
    event = ReferenceField('Event')
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

    def to_dict(self, with_details=False):
        return {
            'from_user': self.from_user.to_dict(),
            'to_user': self.to_user.to_dict(),
            'event': self.event.to_dict(with_details=with_details) if self.event else None,
            'points': self.points,
            'message': self.message,
        }
