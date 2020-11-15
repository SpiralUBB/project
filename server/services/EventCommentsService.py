from typing import Union, List

from mongoengine import DoesNotExist

from models.Event import Event
from models.EventComment import EventComment

from models.User import User
from validators.EventCommentValidator import EventCommentValidator


class EventCommentsService:
    def __init__(self, validator: EventCommentValidator):
        self.validator = validator

    def build_filter_options(self, **kwargs):
        filter_options = {}

        author = kwargs.get('author', None)
        if author is not None:
            filter_options['author'] = author

        event = kwargs.get('event', None)
        if event is not None:
            filter_options['event'] = event

        comment_id = kwargs.get('comment_id', None)
        if comment_id is not None:
            filter_options['id'] = comment_id

        return filter_options

    def add(self, author: User, event: Event, text: str) -> EventComment:
        self.validator.validate_parameters(author, event, text)

        event_comment = EventComment(author=author, event=event, text=text)
        event_comment.save()

        return event_comment

    def find_one_by(self, **kwargs) -> Union[EventComment, None]:
        filter_options = self.build_filter_options(**kwargs)

        try:
            return EventComment.objects.get(**filter_options)
        except DoesNotExist:
            return None

    def find_by(self, **kwargs) -> List[EventComment]:
        filter_options = self.build_filter_options(**kwargs)
        return EventComment.objects(**filter_options)

    def update(self, event_comment: EventComment, text: str = None) -> EventComment:
        if text is not None:
            self.validator.validate_text(text)
            event_comment.text = text

        event_comment.save()

        return event_comment

    def delete(self, event_comment: EventComment):
        event_comment.delete()
