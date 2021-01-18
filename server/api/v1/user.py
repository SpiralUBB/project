from flask import Blueprint, jsonify, request, Flask, Response

from api.v1.helpers import retrieve_logged_in_user, set_new_tokens, unset_tokens
from services.UserFeedbackService import UserFeedbackService
from services.UserService import UserService
from utils.errors import UserLoginFailed
from utils.pagination import get_paginated_items_from_qs

api = Blueprint('api_v1_user', __name__)


@api.route('')
@retrieve_logged_in_user()
def user_get():
    user = request.user
    return jsonify(user.to_dict())


@api.route('/login', methods=['POST'])
def login_post(service: UserService):
    username = request.json.get('username')
    password = request.json.get('password')

    user = service.find_one_by(username=username)
    if user is None:
        raise UserLoginFailed()

    service.verify_password(user, password)

    response = jsonify(user.to_dict())
    set_new_tokens(response, username)

    return response


@api.route('/feedbacks', methods=['GET'])
@retrieve_logged_in_user()
def feedbacks_get(user_feedback_service: UserFeedbackService):
    user = request.user

    feedbacks = user_feedback_service.find_by(to_user=user)

    return jsonify(get_paginated_items_from_qs(feedbacks, with_event=True, with_from_user=True))


@api.route('/logout', methods=['POST'])
@retrieve_logged_in_user()
def logout_post():
    response = Response()
    unset_tokens(response)
    return response


@api.route('/register', methods=['POST'])
def register_post(service: UserService):
    username = request.json.get('username')
    password = request.json.get('password')
    first_name = request.json.get('first_name')
    last_name = request.json.get('last_name')

    user = service.add(username, password, first_name, last_name)
    return jsonify(user.to_dict())


def register_blueprint(app: Flask, prefix: str):
    app.register_blueprint(api, url_prefix=prefix)
