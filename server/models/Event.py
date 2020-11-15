from mongoengine import Document, ReferenceField, IntField, StringField, PointField

from utils.DualMap import DualMap

#
# WARNING
# Do not modify the indices of the following dicts
#

EVENT_VISIBILITY_PUBLIC = 'public'
EVENT_VISIBILITY_PRIVATE = 'private'
EVENT_VISIBILITY_WHITELIST = 'whitelist'

event_visibility_map = DualMap({
    0: EVENT_VISIBILITY_PUBLIC,
    1: EVENT_VISIBILITY_PRIVATE,
    2: EVENT_VISIBILITY_WHITELIST,
}, (-1, 'unknown'))


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
}, (-1, 'Unknown'))


class Event(Document):
    owner = ReferenceField('User', required=True)
    title = StringField(required=True)
    location = StringField()
    location_point = PointField()
    date = StringField(required=True)
    description = StringField(required=True)
    visibility = IntField(min_value=event_visibility_map.minimum_key(),
                          max_value=event_visibility_map.maximum_key(), required=True)
    category = IntField(min_value=event_category_map.minimum_key(),
                        max_value=event_category_map.maximum_key(), required=True)

    def to_dict(self):
        #
        # HACK: location point is list when the object was created, but gets saved
        # as a dict with a coordinates key containing the list
        #
        if isinstance(self.location_point, list):
            location_points = self.location_point
        elif isinstance(self.location_point, dict):
            location_points = self.location_point['coordinates']
        else:
            location_points = None

        return {
            'id': str(self.id),
            'owner': self.owner.to_dict(),
            'title': self.title,
            'location': self.location,
            'location_points': location_points,
            'date': self.date,
            'description': self.description,
            'visibility': self.visibility,
            'visibility_text': event_visibility_map.to_value(self.visibility),
            'category': self.category,
            'category_text': event_category_map.to_value(self.category)
        }
