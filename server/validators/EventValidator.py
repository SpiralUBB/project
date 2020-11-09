from utils.errors import IdInvalid, UsernameInvalid, TitleInvalid, LocationInvalid, DateInvalid, DescriptionInvalid, \
    PrivacyInvalid, TypeInvalid
from utils.types import Types

class EventValidator:
    def validate_id(self, value: int):
        if not value:
            raise IdInvalid(message='ID cannot be empty')

    def validate_username(self, value: str):
        if not value:
            raise UsernameInvalid(message='Creator username cannot be empty')

    def validate_title(self, value: str):
        if not value:
            raise TitleInvalid(message='Title cannot be empty')

    def validate_location(self, value: str):
        if not value:
            raise LocationInvalid(message='Location cannot be empty')

    # TODO make sure to convert to date type and validate the format
    def validate_date(self, value: str):
        if not value:
            raise DateInvalid(message='Date cannot be empty')

    def validate_description(self, value: str):
        if not value:
            raise DescriptionInvalid(message='ID cannot be empty')

    def validate_privacy(self, value: str):
        if not value:
            raise PrivacyInvalid(message='Privacy type cannot be empty')
        types = Types()
        if value not in types.privacy_types:
            raise PrivacyInvalid(message='Invalid privacy type')

    def validate_type(self, value: str):
        if not value:
            raise TypeInvalid(message='Type cannot be empty')
        types = Types()
        if value not in types.event_types:
            raise PrivacyInvalid(message='Invalid event type')

    def validate_parameters(self, id: int, username: str, title: str, location: str, date: str, description: str,
                            privacy: str, ev_type: str):
        self.validate_id(id)
        self.validate_username(username)
        self.validate_title(title)
        self.validate_location(location)
        self.validate_date(date)
        self.validate_description(description)
        self.validate_privacy(privacy)
        self.validate_type(ev_type)
