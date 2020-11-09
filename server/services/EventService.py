from typing import Union

from mongoengine import DoesNotExist

from models.Event import Event

from utils.errors import EventAlreadyExistsError, EventDoesNotExist, AddEventFailed, DeleteEventFailed, ReadEventFailed,\
    UpdateEventFailed
from validators.EventValidator import EventValidator


class EventService:
    def __init__(self, validator: EventValidator):
        self.validator = validator

    def add(self, id: int, username: str, title: str, location: str, date: str, description: str,
                            privacy: str, ev_type: str) -> Event:
        self.validator.validate_parameters(id, username, title, location, date, description, privacy, ev_type)

        try:
            Event.objects.get(id=id)
            raise EventAlreadyExistsError(id)
        except DoesNotExist:
            pass

        event = Event(id=id, username=username, title=title, location=location, date=date, description=description,
                      privacy=privacy, ev_type=ev_type)
        event.save()
        return event

    def find_by(self, id: int) -> Union[Event, None]:
        try:
            return Event.objects.get(id=id)
        except DoesNotExist:
            return None
