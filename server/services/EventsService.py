from typing import Union, List

from mongoengine import DoesNotExist

from models.Event import Event

from models.User import User
from validators.EventValidator import EventValidator


class EventsService:
    def __init__(self, validator: EventValidator):
        self.validator = validator

    def build_filter_options(self, **kwargs):
        filter_options = {}

        event_id = kwargs.get('event_id', None)
        if event_id is not None:
            filter_options['id'] = event_id

        owner = kwargs.get('owner', None)
        if owner is not None:
            filter_options['owner'] = owner

        return filter_options

    def add(self, owner: User, title: str, location: str, date: str, description: str,
            visibility: Union[str, int], category: [str, int]) -> Event:
        visibility = self.validator.parse_visibility(visibility)
        category = self.validator.parse_category(category)

        self.validator.validate_parameters(owner, title, location, date, description)

        event = Event(owner=owner, title=title, location=location, date=date, description=description,
                      visibility=visibility, category=category)
        event.save()

        return event

    def find_by(self, **kwargs) -> Union[Event, None]:
        filter_options = self.build_filter_options(**kwargs)

        try:
            return Event.objects.get(**filter_options)
        except DoesNotExist:
            return None

    def find_all(self) -> List[Event]:
        return Event.objects()

    def update(self, event, title: str, location: str, date: str, description: str,
               visibility: Union[str, int], category: [str, int]) -> Event:
        if title is not None:
            self.validator.validate_title(title)
            event.title = title

        if location is not None:
            self.validator.validate_location(location)
            event.location = location

        if date is not None:
            self.validator.validate_date(date)
            event.date = date

        if description is not None:
            self.validator.validate_description(description)
            event.description = description

        if visibility is not None:
            visibility = self.validator.parse_visibility(visibility)
            event.visibility = visibility

        if category is not None:
            category = self.validator.parse_category(category)
            event.category = category

        event.save()

        return event

    def delete(self, event):
        event.delete()