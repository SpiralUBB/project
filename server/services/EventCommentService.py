from typing import Union, List

from mongoengine import DoesNotExist

from models.Event import Event
from models.EventComment import EventComment

from models.User import User
from validators.EventCommentValidator import EventCommentValidator


class EventCommentService:
    def __init__(self, validator: EventCommentValidator):
        self.validator = validator

    def add(self, author: User, event: Event, text: str) -> EventComment:
        self.validator.validate_parameters(author, event, text)

        event_comment = EventComment(author=author, event=event, text=text)
        event_comment.save()

        return event_comment

    def find_one_by(self, *args, **kwargs) -> Union[EventComment, None]:
        try:
            return EventComment.objects.get(*args, **kwargs)
        except DoesNotExist:
            return None

    def find_by(self, *args, **kwargs):
        return EventComment.objects(*args, **kwargs)

    def update(self, event_comment: EventComment, text: str = None):
        if text is not None:
            self.validator.validate_text(text)
            event_comment.text = text

        event_comment.save()

    def delete(self, event_comment: EventComment):
        event_comment.delete()
