from utils.errors import UsernameInvalid, PasswordInvalid, FirstNameInvalid, LastNameInvalid


class UserValidator:
    def validate_username(self, value: str):
        if not value:
            raise UsernameInvalid(message='Username cannot be empty')

    def validate_password(self, value: str):
        if not value:
            raise PasswordInvalid(message='Password cannot be empty')

    def validate_first_name(self, value: str):
        if not value:
            raise FirstNameInvalid(message='First name cannot be empty')

    def validate_last_name(self, value: str):
        if not value:
            raise LastNameInvalid(message='Last name cannot be empty')

    def validate_parameters(self, username: str, password: str, first_name: str, last_name: str):
        self.validate_username(username)
        self.validate_password(password)
        self.validate_first_name(first_name)
        self.validate_last_name(last_name)
