from datetime import datetime

from mongoengine import Document, ReferenceField, DateTimeField, StringField, CASCADE


class EventComment(Document):
    author = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    event = ReferenceField('Event', required=True, reverse_delete_rule=CASCADE)
    time = DateTimeField(default=datetime.now)
    text = StringField(required=True)

    def to_dict(self, with_event: bool = False):
        d = {
            'id': str(self.id),
            'author': self.author.to_dict(),
            'time': self.time.isoformat(),
            'text': self.text,
        }

        if with_event:
            d['event'] = self.event.to_dict()

        return d
