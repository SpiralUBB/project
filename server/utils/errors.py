class HttpError(Exception):
    def __init__(self, message, code, status):
        super().__init__(message)

        self.code = code
        self.status = status
        self.message = message

    def to_dict(self):
        return {
            'code': self.code,
            'message': self.message,
        }


class UserAlreadyExistsError(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'User already exists'

        super().__init__(message, 'user-already-exists', 403)


class UserDoesNotExist(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'User does not exist'

        super().__init__(message, 'user-not-exist', 404)


class UsernameInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Username is invalid'

        super().__init__(message, 'username-invalid', 400)


class PasswordInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Password is invalid'

        super().__init__(message, 'password-invalid', 400)


class FirstNameInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'First name is invalid'

        super().__init__(message, 'first-name-invalid', 400)


class LastNameInvalid(HttpError):
    def __init__(self, message=None):
        if not message:
            message = 'Last name is invalid'

        super().__init__(message, 'last-name-invalid', 400)


class LoginFailed(HttpError):
    def __init__(self):
        super().__init__('Login failed', 'login-failed', 401)
