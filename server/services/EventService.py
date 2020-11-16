from typing import Union, List

from bson import ObjectId
from mongoengine import DoesNotExist, Q

from models.Event import Event, event_visibility_map, EVENT_VISIBILITY_PUBLIC, EVENT_VISIBILITY_WHITELISTED, \
    EVENT_VISIBILITY_UNLISTED

from models.User import User
from utils.errors import EventInvitationCannotJoinOwn, EventInvitationCannotJoinFull
from validators.EventValidator import EventValidator


class EventService:
    def __init__(self, validator: EventValidator):
        self.validator = validator

    def add(self, owner: User, title: str, location: str, location_point: List[float], date: str,
            no_max_participants: int, description: str, visibility: Union[str, int], category: [str, int]) -> Event:
        visibility = self.validator.parse_visibility(visibility)
        category = self.validator.parse_category(category)

        self.validator.validate_parameters(owner, title, location, location_point, date, no_max_participants,
                                           description)

        event = Event(owner=owner, title=title, location=location, location_point=location_point, date=date,
                      no_max_participants=no_max_participants, description=description, visibility=visibility,
                      category=category)
        event.save()

        return event

    def find_one_by(self, *args, **kwargs) -> Union[Event, None]:
        try:
            return Event.objects.get(*args, **kwargs)
        except DoesNotExist:
            return None

    def find_by(self, *args, **kwargs):
        return Event.objects(*args, **kwargs)

    def build_query_visible_for_user(self, user: User = None, ids=None, show_whitelist: bool = False,
                                     show_unlisted: bool = False):
        if ids is None:
            ids = []

        query = Q()

        # Add public events
        query |= Q(visibility=event_visibility_map.to_key(EVENT_VISIBILITY_PUBLIC))

        if show_whitelist:
            # Add whitelisted events
            query |= Q(visibility=event_visibility_map.to_key(EVENT_VISIBILITY_WHITELISTED))

        if show_unlisted:
            # Add unlisted events
            query |= Q(visibility=event_visibility_map.to_key(EVENT_VISIBILITY_UNLISTED))

        # Add events for which the user has an accepted invite
        query |= Q(id__in=ids)

        if user is not None:
            # Add events owned by the logged in user
            query |= Q(owner=user)

        return query

    def is_details_visible(self, event: Event, user: User, visible_ids: List[ObjectId]):
        if event_visibility_map.to_key(EVENT_VISIBILITY_PUBLIC) == event.visibility:
            return True

        if user is not None and event.owner.id == user.id:
            return True

        if event.id in visible_ids:
            return True

        return False

    def check_can_user_join_event(self, event: Event, user: User):
        if event.owner.id == user.id:
            raise EventInvitationCannotJoinOwn()

        if event.no_max_participants != 0 and event.no_participants >= event.no_max_participants:
            raise EventInvitationCannotJoinFull()

    def find_visible_for_user(self, user: User, ids: List[ObjectId], show_whitelist: bool = False,
                              show_unlisted: bool = False):
        query = self.build_query_visible_for_user(user, ids, show_whitelist, show_unlisted)
        return self.find_by(query)

    def find_one_visible_for_user(self, user: User, event_id: str, ids: List[ObjectId], show_whitelist: bool = False,
                                  show_unlisted: bool = False):
        query = self.build_query_visible_for_user(user, ids, show_whitelist, show_unlisted)
        return self.find_one_by(Q(id=event_id) & query)

    def update(self, event: Event, title: str = None, location: str = None, location_point: List[int] = None,
               date: str = None, no_max_participants: int = None, description: str = None,
               visibility: Union[str, int] = None, category: [str, int] = None):
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

        if no_max_participants is not None:
            self.validator.validate_no_max_participants(no_max_participants)
            event.no_max_participants = no_max_participants

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
