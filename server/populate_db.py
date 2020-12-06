#!/usr/bin/env python3

from mongoengine import connect

from config import DB_USERNAME, DB_NAME, DB_PASSWORD, DB_HOST
from models.Event import event_visibility_map
from services.EventCommentService import EventCommentService
from services.EventService import EventService
from services.UserService import UserService
from utils.dependencies import services_injector
from utils.errors import UserAlreadyExists

connect(
    db=DB_NAME,
    username=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOST,
)

user_service = services_injector.get(UserService)
event_service = services_injector.get(EventService)
event_comment_service = services_injector.get(EventCommentService)

try:
    admin_user = user_service.add('admin', 'pass', 'Admin', 'Name')
    user_service.add_points(admin_user, 300)
except UserAlreadyExists:
    admin_user = user_service.find_one_by(username='admin')

try:
    test_user = user_service.add('test_user', 'pass', 'Test', 'User')
    user_service.add_points(test_user, 100)
except UserAlreadyExists:
    test_user = user_service.find_one_by(username='test_user')

events = []

for user in [test_user, admin_user]:
    for visibility in event_visibility_map.keys():
        event = event_service.add(admin_user,
                                  'Beuta {}'.format(event_visibility_map.to_value(visibility)),
                                  'Infinity', [-23.0, 54.0],
                                  '2021-11-29T00:00:00.000000+02:00', '2021-11-29T08:30:00.000000Z',
                                  0, 30,
                                  'Hai cu noi la bere',
                                  visibility,
                                  'Food & Drink')
        events.append(event)

for event in events:
    for i in range(5):
        for user in [test_user, admin_user]:
            event_comment_service.add(user, event, 'This is a comment by admin for event {}'.format(i))
            event_comment_service.add(user, event, 'This is a comment by test user for event {}'.format(i))
