from enum import Enum
from typing import Union, List

from bson import ObjectId
from mongoengine import DoesNotExist, Q
from pyee import BaseEventEmitter

from models.Event import Event, EVENT_VISIBILITY_PUBLIC_KEY, EVENT_VISIBILITY_WHITELISTED_KEY, \
    EVENT_VISIBILITY_UNLISTED_KEY
from models.EventInvitation import EVENT_INVITATION_STATUS_PENDING_KEY, \
    EVENT_INVITATION_STATUS_ACCEPTED_KEY, EVENT_INVITATION_STATUS_DENIED_KEY

from models.User import User
from validators.EventValidator import EventValidator


class EventServiceEvents(Enum):
    EVENT_ADDED = 'event-added'
    EVENT_DELETED = 'event-deleted'


class EventService:
    def __init__(self, validator: EventValidator):
        self.validator = validator
        self.emitter = BaseEventEmitter()

    def add(self, owner: User, title: str, location: str, location_point: List[float], start_time: str, end_time: str,
            min_trust_level: int, no_max_participants: int, description: str, visibility: Union[str, int],
            category: [str, int]) -> Event:
        visibility = self.validator.parse_visibility(visibility)
        category = self.validator.parse_category(category)
        start_time = self.validator.parse_time(start_time)
        end_time = self.validator.parse_time(end_time)

        self.validator.validate_parameters(owner, title, location, location_point, start_time, end_time,
                                           min_trust_level, no_max_participants, description)

        event = Event(owner=owner, title=title, location=location, location_point=location_point, start_time=start_time,
                      end_time=end_time, no_max_participants=no_max_participants, description=description,
                      visibility=visibility, category=category)
        event.save()

        self.emitter.emit(EventServiceEvents.EVENT_ADDED, event)

        return event

    def add_participants(self, event: Event, no_participants: int = 0, old_invitation_status: int = None,
                         new_invitation_status: int = None):
        event_transition_participants = [
            (EVENT_INVITATION_STATUS_DENIED_KEY, EVENT_INVITATION_STATUS_ACCEPTED_KEY, 1),
            (EVENT_INVITATION_STATUS_ACCEPTED_KEY, EVENT_INVITATION_STATUS_DENIED_KEY, -1),
            (EVENT_INVITATION_STATUS_PENDING_KEY, EVENT_INVITATION_STATUS_ACCEPTED_KEY, 1),
            (EVENT_INVITATION_STATUS_ACCEPTED_KEY, EVENT_INVITATION_STATUS_PENDING_KEY, -1),
        ]

        if old_invitation_status is not None and new_invitation_status is not None:
            for from_key, to_key, change in event_transition_participants:
                if old_invitation_status == from_key and new_invitation_status == to_key:
                    no_participants += change

        Event.objects(id=event.id).update_one(inc__no_participants=no_participants)
        event.reload()

    def find_one_by(self, *args, **kwargs) -> Union[Event, None]:
        try:
            return Event.objects.get(*args, **kwargs)
        except DoesNotExist:
            return None

    def find_by(self, *args, **kwargs):
        return Event.objects(*args, **kwargs)

    def build_query_filters(self, categories: List[Union[int, str]] = None, date_start: str = None,
                            date_end: str = None, ids: List[ObjectId] = None, owner: User = None,
                            exclude_owner: bool = False):
        query = Q()

        if categories:
            categories = [self.validator.parse_category(c) for c in categories]
            query &= Q(category__in=categories)

        if date_start:
            date_start = self.validator.parse_time(date_start, start=True)
            query &= Q(start_time__gte=date_start)

        if date_end:
            date_end = self.validator.parse_time(date_end, end=True)
            query &= Q(start_time__lte=date_end)

        if owner:
            if exclude_owner:
                query &= Q(owner__ne=owner)
            else:
                query &= Q(owner=owner)

        if ids is not None:
            query &= Q(id__in=ids)

        return query

    def build_query_visible(self, user: User, ids: List[ObjectId] = None, show_public: bool = False,
                            show_whitelist: bool = False, show_unlisted: bool = False):
        query = Q()

        if user:
            # Add events owned by the logged in user
            query |= Q(owner=user)

        if ids:
            # Add events for which the user has an accepted invite
            query |= Q(id__in=ids)

        if show_public:
            # Add public events
            query |= Q(visibility=EVENT_VISIBILITY_PUBLIC_KEY)

        if show_whitelist:
            # Add whitelisted events
            query |= Q(visibility=EVENT_VISIBILITY_WHITELISTED_KEY)

        if show_unlisted:
            # Add unlisted events
            query |= Q(visibility=EVENT_VISIBILITY_UNLISTED_KEY)

        return query

    def is_details_visible(self, event: Event, user: User, visible_ids: List[ObjectId]):
        if EVENT_VISIBILITY_PUBLIC_KEY == event.visibility:
            return True

        if user is not None and event.owner.id == user.id:
            return True

        if event.id in visible_ids:
            return True

        return False

    def find_visible_for_user(self, user: User, ids: List[ObjectId], show_public: bool = False,
                              show_whitelist: bool = False, show_unlisted: bool = False,
                              categories: List[Union[int, str]] = None, date_start: str = None, date_end: str = None,
                              filter_ids: List[ObjectId] = None, filter_owner: User = None,
                              filter_exclude_owner: bool = False, sort_newest_first: bool = False):
        query = Q()
        query &= self.build_query_filters(categories, date_start, date_end, filter_ids, filter_owner,
                                          filter_exclude_owner)
        query &= self.build_query_visible(user, ids, show_public, show_whitelist, show_unlisted)

        queryset = self.find_by(query)
        if sort_newest_first:
            queryset = queryset.order_by('-id')

        return queryset

    def find_one_visible_for_user(self, user: User, event_id: str, ids: List[ObjectId], show_public: bool = False,
                                  show_whitelist: bool = False, show_unlisted: bool = False):
        query = Q()
        query &= self.build_query_visible(user, ids, show_public, show_whitelist, show_unlisted)
        query &= Q(id=event_id)
        return self.find_one_by(query)

    def update(self, event: Event, title: str = None, location: str = None, location_point: List[int] = None,
               start_time: str = None, end_time: str = None, min_trust_level: int = None,
               no_max_participants: int = None, description: str = None, visibility: Union[str, int] = None,
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

        if start_time is not None or end_time is not None:
            if start_time is not None:
                start_time = self.validator.parse_time(start_time)
            else:
                start_time = event.start_time

            if end_time is not None:
                end_time = self.validator.parse_time(end_time)
            else:
                end_time = event.end_time

            self.validator.validate_times(start_time, end_time)

        if min_trust_level is not None:
            self.validator.validate_min_trust_level(min_trust_level, event.owner)
            event.min_trust_level = min_trust_level

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

        self.emitter.emit(EventServiceEvents.EVENT_DELETED, event)
