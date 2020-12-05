from flask import Blueprint, jsonify, request, Flask, Response
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, get_jwt_identity, \
    unset_access_cookies, create_refresh_token, jwt_refresh_token_required, unset_refresh_cookies, set_refresh_cookies

from api.v1.helpers import retrieve_logged_in_user
from services.UserService import UserService
from utils.errors import UserLoginFailed

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
    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response


@api.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh_post():
    username = get_jwt_identity()
    response = Response()
    access_token = create_access_token(identity=username)
    set_access_cookies(response, access_token)
    return response


@api.route('/logout', methods=['POST'])
@jwt_required
def logout_post():
    response = Response()
    unset_access_cookies(response)
    unset_refresh_cookies(response)
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
