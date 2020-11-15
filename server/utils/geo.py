from typing import List

from config import GEOGRAPHICAL_APPROXIMATION_DIGITS, GEOGRAPHICAL_APPROXIMATION_METERS


def approximate_location(points: List[float]):
    return [round(point, GEOGRAPHICAL_APPROXIMATION_DIGITS) for point in points], GEOGRAPHICAL_APPROXIMATION_METERS
