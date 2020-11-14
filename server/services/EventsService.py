from typing import Union, List

from mongoengine import DoesNotExist

from models.Event import Event

from models.User import User
from validators.EventValidator import EventValidator


class EventsService:
    def __init__(self, validator: EventValidator):
        self.validator = validator

    def add(self, owner: User, title: str, location: str, date: str, description: str,
            visibility: Union[str, int], category: [str, int]) -> Event:
        visibility = self.validator.parse_visibility(visibility)
        category = self.validator.parse_category(category)

        self.validator.validate_parameters(owner, title, location, date, description)

        event = Event(owner=owner, title=title, location=location, date=date, description=description,
                      visibility=visibility, category=category)
        event.save()

        return event

    def find_by(self, event_id: str) -> Union[Event, None]:
        try:
            return Event.objects.get(id=event_id)
        except DoesNotExist:
            return None

    def find_all(self) -> List[Event]:
        return Event.objects()
