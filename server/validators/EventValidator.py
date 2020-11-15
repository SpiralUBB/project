from typing import List

from models.Event import event_visibility_map, event_category_map
from models.User import User
from utils.errors import UserUsernameInvalid, EventTitleInvalid, EventLocationInvalid, EventDateInvalid, \
    EventDescriptionInvalid, EventCategoryInvalid, EventLocationPointInvalid, EventOwnerInvalid


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

    def validate_location_point(self, value: List[int]):
        if not value:
            raise EventLocationPointInvalid(message='Event location point cannot be empty')

        if type(value) != list:
            raise EventLocationPointInvalid(message='Event location point must be a list')

        if len(value) != 2:
            raise EventLocationPointInvalid(message='Event location point must be a list with 2 values')

        for x in value:
            if type(x) != float:
                raise EventLocationPointInvalid(message='Event location point must be a list with 2 floats')

    def validate_date(self, value: str):
        if not value:
            raise EventDateInvalid(message='Event date cannot be empty')

    def validate_description(self, value: str):
        if not value:
            raise EventDescriptionInvalid(message='Event description cannot be empty')

    def parse_visibility(self, value):
        if value is None:
            raise EventCategoryInvalid(message='Event visibility cannot be empty')

        try:
            value = int(value)
        except ValueError:
            pass

        value = event_visibility_map.to_key_either(value)
        if value is None:
            raise EventCategoryInvalid(message='Event visibility cannot be found inside the predefined list')

        return value

    def parse_category(self, value):
        try:
            value = int(value)
        except ValueError:
            pass

        value = event_category_map.to_key_either(value)
        if value is None:
            raise EventCategoryInvalid(message='Event category cannot be found inside the predefined list')

        return value

    def validate_parameters(self, owner: User, title: str, location: str, location_point: List[int],
                            date: str, description: str):
        self.validate_owner(owner)
        self.validate_title(title)
        self.validate_location(location)
        self.validate_location_point(location_point)
        self.validate_date(date)
        self.validate_description(description)
