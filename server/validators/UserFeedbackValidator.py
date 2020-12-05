from utils.errors import UserFeedbackPointsInvalid


class UserFeedbackValidator:
    def parse_points(self, value):
        if value is None:
            raise UserFeedbackPointsInvalid('User feedback points cannot be empty')

        try:
            value = int(value)
        except ValueError:
            raise UserFeedbackPointsInvalid('User feedback points must be a number')

        if value < -6 or value > 6:
            raise UserFeedbackPointsInvalid('User feedback points must be between -6 and 6')

        return value
