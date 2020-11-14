#!/usr/bin/env python3

from mongoengine import connect

from config import DB_USERNAME, DB_NAME, DB_PASSWORD, DB_HOST
from services.UserService import UserService
from services.EventsService import EventsService
from utils.errors import UserAlreadyExistsError
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

try:
    adminUser = userService.add("admin", "pass", "Admin", "Name")
except UserAlreadyExistsError:
    adminUser = userService.find_by(username="admin")

eventValidator = EventValidator()
eventService = EventsService(eventValidator)
eventService.add(adminUser, "Beuta", "Infinity", "27/11/2020-22:00", "Hai cu noi la bere", "private", "Food & Drink")
