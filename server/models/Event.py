from mongoengine import Document, ReferenceField, IntField, StringField, PointField

from utils.DualMap import DualMap

#
# WARNING
# Do not modify the indices of the following dicts
#

event_visibility_map = DualMap({
    0: 'private',
    1: 'public',
    2: 'whitelist',
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
        if self.location_point is not None:
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
