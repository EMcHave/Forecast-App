from lines_for_user import *


class InvalidInputError(Exception):
    message : str = WRONG_INPUT_LINE


class EmptyInputError(Exception):
    message : str = EMPTY_INPUT_LINE


class LocationError(Exception):
    message : str = UNKNOWN_GEOLOCATION_LINE


class APIRequestError(Exception):
    message : str = FAILED_API_REQUEST_LINE


CUSTOM_EXCEPTIONS = (InvalidInputError,
                     EmptyInputError,
                     LocationError,
                     APIRequestError)
