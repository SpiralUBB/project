from typing import List

from mongoengine import Document, ReferenceField, IntField, StringField, PointField, DateTimeField, CASCADE

from config import GEOGRAPHICAL_APPROXIMATION_DIGITS, GEOGRAPHICAL_APPROXIMATION_METERS
from utils.DualMap import DualMap

#
# WARNING
# Do not modify the indices of the following dicts
#
EVENT_VISIBILITY_PUBLIC_KEY = 0
EVENT_VISIBILITY_UNLISTED_KEY = 1
EVENT_VISIBILITY_WHITELISTED_KEY = 2

event_visibility_map = DualMap({
    EVENT_VISIBILITY_PUBLIC_KEY: 'public',
    EVENT_VISIBILITY_UNLISTED_KEY: 'unlisted',
    EVENT_VISIBILITY_WHITELISTED_KEY: 'whitelisted',
}, (-1, 'unknown-visibility'))


event_category_map = DualMap({
    0: 'Arts',
    1: 'Book Clubs',
    2: 'Business',
    3: 'Family',
    4: 'Fashion',
    5: 'Film',
    6: 'Food & Drink',
    7: 'Games',
    8: 'Hobbies & Crafts',
    9: 'Learning',
    10: 'Music',
    11: 'Outdoors & Adventure',
    12: 'Partying',
    13: 'Social',
    14: 'Sport & Fitness',
    15: 'Tech',
}, (-1, 'unknown-category'))


class Event(Document):
    owner = ReferenceField('User', required=True, reverse_delete_rule=CASCADE)
    title = StringField(required=True)
    location = StringField()
    location_point = PointField()
    start_time = DateTimeField(required=True)
    end_time = DateTimeField(required=True)
    no_participants = IntField(min_value=0, default=0)
    no_max_participants = IntField(min_value=0, default=0)
    description = StringField(required=True)
    min_trust_level = IntField(min_value=0, default=0)
    visibility = IntField(min_value=event_visibility_map.minimum_key(),
                          max_value=event_visibility_map.maximum_key(), required=True)
    category = IntField(min_value=event_category_map.minimum_key(),
                        max_value=event_category_map.maximum_key(), required=True)

    def is_unlimited_participants(self):
        return self.no_max_participants == 0

    def allows_more_participants(self):
        if self.is_unlimited_participants():
            return True

        if self.no_participants < self.no_max_participants:
            return True

        return False

    def to_dict(self, with_details: bool = False):
        #
        # HACK: location point is list when the object was created, but gets saved
        # as a dict with a coordinates key containing the list
        #
        if isinstance(self.location_point, list):
            location_points = self.location_point
        elif isinstance(self.location_point, dict):
            location_points = self.location_point['coordinates']
        else:
            location_points = []

        d = {
            'id': str(self.id),
            'owner': self.owner.to_dict(),
            'title': self.title,
            'start_time': self.start_time.isoformat(),
            'end_time': self.end_time.isoformat(),
            'description': self.description,
            'visibility': self.visibility,
            'visibility_text': event_visibility_map.to_value(self.visibility),
            'category': self.category,
            'category_text': event_category_map.to_value(self.category),
            'is_limited_details': not with_details,
            'min_trust_level': self.min_trust_level,
        }

        if with_details:
            d['location'] = self.location
            d['location_points'] = location_points
            d['location_points_radius_meters'] = None
            d['no_participants'] = self.no_participants
            d['no_max_participants'] = self.no_max_participants
            d['is_unlimited_participants'] = self.is_unlimited_participants()
            d['allows_more_participants'] = self.allows_more_participants()
        else:
            d['location'] = None
            d['location_points'] = [round(p, GEOGRAPHICAL_APPROXIMATION_DIGITS) for p in location_points]
            d['location_points_radius_meters'] = GEOGRAPHICAL_APPROXIMATION_METERS
            d['no_participants'] = None
            d['no_max_participants'] = None
            d['is_unlimited_participants'] = None
            d['allows_more_participants'] = None

        return d
