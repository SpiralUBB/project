from typing import Union, List

from bson import ObjectId
from mongoengine import DoesNotExist, Q

from models.Event import Event, event_visibility_map, EVENT_VISIBILITY_PUBLIC, EVENT_VISIBILITY_WHITELIST

from models.User import User
from validators.EventValidator import EventValidator


class EventService:
    def __init__(self, validator: EventValidator):
        self.validator = validator

    def add(self, owner: User, title: str, location: str, location_point: List[float], date: str, description: str,
            visibility: Union[str, int], category: [str, int]) -> Event:
        visibility = self.validator.parse_visibility(visibility)
        category = self.validator.parse_category(category)

        self.validator.validate_parameters(owner, title, location, location_point, date, description)

        event = Event(owner=owner, title=title, location=location, location_point=location_point, date=date,
                      description=description, visibility=visibility, category=category)
        event.save()

        return event

    def find_one_by(self, *args, **kwargs) -> Union[Event, None]:
        try:
            return Event.objects.get(*args, **kwargs)
        except DoesNotExist:
            return None

    def find_by(self, *args, **kwargs):
        return Event.objects(*args, **kwargs)

    def build_query_visible_for_user(self, user: User = None, ids=None):
        if ids is None:
            ids = []

        query = Q()

        # Add public events
        query |= Q(visibility=event_visibility_map.to_key(EVENT_VISIBILITY_PUBLIC))

        # Add whitelisted events
        query |= Q(visibility=event_visibility_map.to_key(EVENT_VISIBILITY_WHITELIST))

        # Add events for which the user has an accepted invite
        query |= Q(id__in=ids)

        if user:
            # Add events owned by the logged in user
            query |= Q(owner=user)

        return query

    def is_details_hidden(self, user: User, event: Event, visible_ids: List[ObjectId]):
        # For whitelisted events for which the user doesn't have an accepted invite,
        # and for which the user isn't the owner, we need to restrict the information shown
        return event_visibility_map.to_key(EVENT_VISIBILITY_WHITELIST) == event.visibility \
               and event.id not in visible_ids and event.owner.id != user.id

    def find_visible_for_user(self, user: User, ids):
        return self.find_by(self.build_query_visible_for_user(user, ids))

    def find_one_visible_for_user(self, user: User, event_id: str, ids):
        return self.find_one_by(Q(id=event_id) & self.build_query_visible_for_user(user, ids))

    def update(self, event: Event, title: str = None, location: str = None, location_point: List[int] = None,
               date: str = None, description: str = None, visibility: Union[str, int] = None,
               category: [str, int] = None):
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

    def delete(self, event: Event):
        event.delete()
