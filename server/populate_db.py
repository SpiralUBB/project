#!/usr/bin/env python3

from mongoengine import connect

from config import DB_USERNAME, DB_NAME, DB_PASSWORD, DB_HOST
from services.UserService import UserService
from services.EventService import EventService
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
userService.add("admin", "pass", "Admin", "Name")

eventValidator = EventValidator()
eventService = EventService(eventValidator)
eventService.add("1", "admin", "Beuta", "Infinity", "27/11/2020-22:00", "Hai cu noi la bere", "private", "Food & Drink")
