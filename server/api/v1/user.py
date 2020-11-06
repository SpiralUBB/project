from flask import Blueprint, jsonify, request, Flask, Response
from flask_jwt_extended import create_access_token, set_access_cookies, jwt_required, get_jwt_identity, \
    unset_access_cookies

from services.UserService import UserService
from utils.errors import UserDoesNotExist, LoginFailed

api = Blueprint('api_v1_user', __name__)


@api.route('')
@jwt_required
def user_get(service: UserService):
    username = get_jwt_identity()
    user = service.find_by(username=username)
    if user is None:
        raise UserDoesNotExist()

    return jsonify(user.to_dict())


@api.route('/login', methods=['POST'])
def login_post(service: UserService):
    username = request.json.get('username')
    password = request.json.get('password')

    user = service.find_by(username=username)
    if user is None:
        raise LoginFailed()

    service.verify_password(user, password)

    response = jsonify(user.to_dict())
    access_token = create_access_token(identity=username)
    set_access_cookies(response, access_token)
    return response


@api.route('/logout', methods=['POST'])
@jwt_required
def logout_post():
    response = Response()
    unset_access_cookies(response)
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
