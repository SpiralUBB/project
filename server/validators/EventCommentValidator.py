from models.Event import Event
from models.User import User
from utils.errors import EventCommentAuthorInvalid, EventCommentEventInvalid, EventCommentTextInvalid


class EventCommentValidator:
    def validate_author(self, value: User):
        if not value:
            raise EventCommentAuthorInvalid(message='Event comment author cannot be missing')

    def validate_event(self, value: Event):
        if not value:
            raise EventCommentEventInvalid(message='Event comment event cannot be missing')

    def validate_text(self, value: str):
        if not value:
            raise EventCommentTextInvalid(message='Event description cannot be empty')

    def validate_parameters(self, author: User, event: Event, text: str):
        self.validate_author(author)
        self.validate_event(event)
        self.validate_text(text)
