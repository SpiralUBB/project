#!/usr/bin/env python3

from mongoengine import connect

from config import DB_USERNAME, DB_NAME, DB_PASSWORD, DB_HOST
from services.EventCommentService import EventCommentService
from services.UserService import UserService
from services.EventService import EventService
from utils.errors import UserAlreadyExists
from validators.EventCommentValidator import EventCommentValidator
from validators.UserValidator import UserValidator
from validators.EventValidator import EventValidator

connect(
    db=DB_NAME,
    username=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOST,
)

userValidator = UserValidator()
userService = UserService(userValidator)

eventValidator = EventValidator()
eventService = EventService(eventValidator)

eventCommentValidator = EventCommentValidator()
eventCommentService = EventCommentService(eventCommentValidator)

try:
    adminUser = userService.add("admin", "pass", "Admin", "Name")
except UserAlreadyExists:
    adminUser = userService.find_one_by(username="admin")

eventValidator = EventValidator()
eventService = EventService(eventValidator)
events = []

event = eventService.add(adminUser, "Beuta unlisted", "Infinity", [-23.0, 54.0], "2021-11-29T00:00:00.000000+02:00",
                         "2021-11-29T08:30:00.000000Z", 30, "Hai cu noi la bere", "unlisted", "Food & Drink")
events.append(event)
event = eventService.add(adminUser, "Beuta publica", "Infinity", [-23.0, 54.0], "2021-11-29T00:00:00.000000+02:00",
                         "2021-11-29T08:30:00.000000Z", 30, "Hai cu noi la bere", "public", "Food & Drink")
events.append(event)
event = eventService.add(adminUser, "Beuta cu whitelist", "Infinity", [-23.0, 54.0], "2021-11-29T00:00:00.000000+02:00",
                         "2021-11-29T08:30:00.000000Z", 30, "Hai cu noi la bere", "whitelisted", "Food & Drink")
events.append(event)

for i, event in enumerate(events):
    eventCommentService.add(adminUser, event, "This is a comment for event {}".format(i))
