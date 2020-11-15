from datetime import datetime

from mongoengine import Document, ReferenceField, DateTimeField, StringField


class EventComment(Document):
    author = ReferenceField('User', required=True)
    event = ReferenceField('Event', required=True)
    time = DateTimeField(default=datetime.now)
    text = StringField(required=True)

    def to_dict(self, with_event=False):
        d = {
            'id': self.id,
            'author': self.author.to_dict(),
            'text': self.text,
        }

        if with_event:
            d['event'] = self.event.to_dict()

        return d
