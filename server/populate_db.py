#!/usr/bin/env python3

from mongoengine import connect

from config import DB_USERNAME, DB_NAME, DB_PASSWORD, DB_HOST
from services.UserService import UserService
from validators.UserValidator import UserValidator

connect(
    db=DB_NAME,
    username=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOST,
)

validator = UserValidator()
service = UserService(validator)
service.add("admin", "pass", "Admin", "Name")

