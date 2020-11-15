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

    def add(self, owner: User, title: str, location: str, location_point: List[int], date: str, description: str,
            visibility: Union[str, int], category: [str, int]) -> Event:
        visibility = self.validator.parse_visibility(visibility)
        category = self.validator.parse_category(category)

        self.validator.validate_parameters(owner, title, location, location_point, date, description)

        event = Event(owner=owner, title=title, location=location, location_point=location_point, date=date,
                      description=description, visibility=visibility, category=category)
        event.save()

        return event

    def find_one_by(self, **kwargs) -> Union[Event, None]:
        filter_options = self.build_filter_options(**kwargs)

        try:
            return Event.objects.get(**filter_options)
        except DoesNotExist:
            return None

    def find_by(self, **kwargs) -> List[Event]:
        filter_options = self.build_filter_options(**kwargs)
        return Event.objects(**filter_options)

    def update(self, event: Event, title: str = None, location: str = None, location_point: List[int] = None,
               date: str = None, description: str = None, visibility: Union[str, int] = None,
               category: [str, int] = None) -> Event:
        if title is not None:
            self.validator.validate_title(title)
            event.title = title

        if location is not None:
            self.validator.validate_location(location)
            event.location = location

        if location_point is not None:
            self.validator.validate_location_point(location_point)
            event.location_point = location_point

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

    def delete(self, event: Event):
        event.delete()
