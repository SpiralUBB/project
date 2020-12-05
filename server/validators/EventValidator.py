import arrow

from datetime import datetime
from typing import List, Union

from arrow import ParserError

from models.Event import event_visibility_map, event_category_map
from models.User import User
from utils.errors import EventTitleInvalid, EventLocationInvalid, EventTimeInvalid, \
    EventDescriptionInvalid, EventCategoryInvalid, EventLocationPointInvalid, EventOwnerInvalid, EventVisibilityInvalid, \
    EventMaxNoParticipantsInvalid, EventMinTrustLevelInvalid


class EventValidator:
    def validate_owner(self, value: User):
        if not value:
            raise EventOwnerInvalid(message='Event owner cannot be missing')

    def validate_title(self, value: str):
        if not value:
            raise EventTitleInvalid(message='Event title cannot be empty')

    def validate_location(self, value: str):
        if not value:
            raise EventLocationInvalid(message='Event location cannot be empty')

    def validate_location_point(self, value: List[float]):
        if not value:
            raise EventLocationPointInvalid(message='Event location point cannot be empty')

        if type(value) != list:
            raise EventLocationPointInvalid(message='Event location point must be a list')

        if len(value) != 2:
            raise EventLocationPointInvalid(message='Event location point must be a list with 2 values')

        for x in value:
            if type(x) != float:
                raise EventLocationPointInvalid(message='Event location point must be a list with 2 floats')

    def validate_time(self, value, name):
        if not value:
            raise EventTimeInvalid(message='Event {} time cannot be empty'.format(name))

        if not isinstance(value, datetime):
            raise EventTimeInvalid(message='Event {} time must be a datetime object'.format(name))

    def validate_times(self, start, end):
        self.validate_time(start, 'start')
        self.validate_time(end, 'end')

        if start.date() < arrow.utcnow().date():
            raise EventTimeInvalid(message='Event start time cannot be in the past')

        if end.date() < start.date():
            raise EventTimeInvalid(message='Event end time cannot be before event start time')

    def validate_no_max_participants(self, value: int):
        if value is not None:
            if type(value) != int:
                raise EventMaxNoParticipantsInvalid(
                    message='Event max number of participants must either be omitted or be a number')

            if value < 0:
                raise EventMaxNoParticipantsInvalid(
                    message='Event max number of participants must be a number greater or equal to 0')

    def validate_min_trust_level(self, value: int, owner: User):
        if value is not None:
            if type(value) != int:
                raise EventMinTrustLevelInvalid(
                    message='Event min trust level must either be omitted or be a number')

            if value < 0:
                raise EventMinTrustLevelInvalid(
                    message='Event min trust level must be a number greater or equal to 0')

            if value > owner.get_trust_level():
                raise EventMinTrustLevelInvalid(
                    message='Event trust level cannot be greater than owner trust level')

    def validate_description(self, value: str):
        if not value:
            raise EventDescriptionInvalid(message='Event description cannot be empty')

    def parse_visibility(self, value):
        if value is None:
            raise EventVisibilityInvalid(message='Event visibility cannot be empty')

        try:
            value = int(value)
        except ValueError:
            pass

        value = event_visibility_map.to_key_either(value)
        if value < 0:
            raise EventVisibilityInvalid(message='Event visibility cannot be found inside the predefined list')

        return value

    def parse_category(self, value):
        if value is None:
            raise EventCategoryInvalid(message='Event category cannot be empty')

        try:
            value = int(value)
        except ValueError:
            pass

        value = event_category_map.to_key_either(value)
        if value < 0:
            raise EventCategoryInvalid(message='Event category cannot be found inside the predefined list')

        return value

    def parse_time(self, value: str, start=False, end=False) -> Union[datetime, None]:
        if not value:
            return None

        try:
            time = arrow.get(value)
            if start:
                time = time.replace(hour=0, minute=0)
            elif end:
                time = time.replace(hour=23, minute=59)

            return time.to('utc').datetime
        except ParserError:
            raise EventTimeInvalid(message="Event time couldn't be parsed into a valid date-time format")

    def validate_parameters(self, owner: User, title: str, location: str, location_point: List[float],
                            start_time: datetime, end_time: datetime, min_trust_level: int, no_max_participants: int,
                            description: str):
        self.validate_owner(owner)
        self.validate_title(title)
        self.validate_location(location)
        self.validate_location_point(location_point)
        self.validate_times(start_time, end_time)
        self.validate_min_trust_level(min_trust_level, owner)
        self.validate_no_max_participants(no_max_participants)
        self.validate_description(description)
