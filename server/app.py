#!/usr/bin/env python3

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_injector import FlaskInjector
from mongoengine import connect

from api.v1.api_v1 import register_blueprint as register_api_v1_blueprint
from config import DB_NAME, DB_USERNAME, DB_PASSWORD, DB_HOST, JWT_SECRET_KEY, JWT_TOKEN_LOCATION, \
    JWT_COOKIE_CSRF_PROTECT
from utils.dependencies import configure_services
from utils.errors import HttpError

connect(
    db=DB_NAME,
    username=DB_USERNAME,
    password=DB_PASSWORD,
    host=DB_HOST,
)

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = JWT_SECRET_KEY
app.config['JWT_TOKEN_LOCATION'] = JWT_TOKEN_LOCATION
app.config['JWT_COOKIE_CSRF_PROTECT'] = JWT_COOKIE_CSRF_PROTECT
JWTManager(app)

register_api_v1_blueprint(app, '/api/v1')

FlaskInjector(app=app, modules=[configure_services])


@app.errorhandler(HttpError)
def http_errorhandler(e):
    return jsonify(e.to_dict()), e.status

