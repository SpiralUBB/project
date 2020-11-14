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
})


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
})


class Event(Document):
    owner = ReferenceField('User')
    title = StringField()
    location = StringField()
    location_point = PointField()
    date = StringField()
    description = StringField()
    visibility = IntField(min_value=event_visibility_map.minimum_key(),
                          max_value=event_visibility_map.maximum_key())
    category = IntField(min_value=event_category_map.minimum_key(),
                        max_value=event_category_map.maximum_key())

    def to_dict(self):
        return {
            'id': str(self.id),
            'owner': self.owner.to_dict(),
            'title': self.title,
            'location': self.location,
            'location_point': self.location_point,
            'date': self.date,
            'description': self.description,
            'visibility': self.visibility,
            'visibility_text': event_visibility_map.to_value(self.visibility),
            'category': self.category,
            'category_text': event_category_map.to_value(self.category)
        }
