class Types:
    def __init__(self):
        self.privacy_types = ['private', 'public', 'whitelist']
        self.event_types = ['Arts', 'Beliefs', 'Book Clubs', 'Career & Business', 'Dance', 'D&D', 'Family', 'Fashion & Beauty',
                       'Film', 'Food & Drink', 'Hobbies & Crafts', 'Language & Culture', 'Learning', 'Movements', 'Music',
                       'Outdoors & Adventure', 'Pets', 'Photography', 'Sci-Fi & Games', 'Social', 'Sport & Fitness', 'Tech',
                       'Writing']

    def getPrivacyTypes(self):
        return self.privacy_types

    def getEventTypes(self):
        return self.event_types
