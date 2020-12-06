#!/usr/bin/env python3
import random

from mongoengine import connect

from config import DB_USERNAME, DB_NAME, DB_PASSWORD, DB_HOST
from models.Event import event_visibility_map
from services.EventCommentService import EventCommentService
from services.EventInvitationService import EventInvitationService
from services.EventService import EventService
from services.UserFeedbackService import UserFeedbackService
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
event_invitation_service = services_injector.get(EventInvitationService)
user_feedback_service = services_injector.get(UserFeedbackService)

users = []

try:
    user = user_service.add('admin', 'pass', 'Admin', 'Name')
    user_service.add_points(user, 300)
except UserAlreadyExists:
    user = user_service.find_one_by(username='admin')

users.append(user)

try:
    user = user_service.add('test_user', 'pass', 'Test', 'User')
    user_service.add_points(user, 100)
except Exception as e:
    print(e)
    user = user_service.find_one_by(username='test_user')

try:
    user = user_service.add('another_user', 'pass', 'Another', 'User')
    user_service.add_points(user, 100)
except Exception as e:
    print(e)
    user = user_service.find_one_by(username='another_user')

users.append(user)

events = []

for user in users:
    for visibility in event_visibility_map.keys():
        event = event_service.add(user,
                                  'Beuta {}'.format(event_visibility_map.to_value(visibility)),
                                  'Infinity', [-23.0, 54.0],
                                  '2021-11-29T00:00:00.000000+02:00', '2021-11-29T08:30:00.000000Z',
                                  0, 30,
                                  'Hai cu noi la bere',
                                  visibility,
                                  'Food & Drink')
        events.append(event)

for event in events:
    for user in users:
        try:
            event_invitation_service.add(event, user)
        except Exception as e:
            print(e)
            pass

for from_user in users:
    for to_user in users:
        if from_user == to_user:
            continue

        for event in events + [None]:
            try:
                points = random.randint(-6, 6)
                message = "You're okay"
                user_feedback_service.add(from_user, to_user, event, points, message)
            except Exception as e:
                print(e)
                pass

for event in events:
    for i in range(5):
        for user in users:
            event_comment_service.add(user, event, 'This is a comment by {}. Hello'.format(user.first_name))
