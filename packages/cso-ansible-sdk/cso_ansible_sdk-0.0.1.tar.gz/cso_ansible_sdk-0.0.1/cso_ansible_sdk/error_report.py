from requests.exceptions import HTTPError

from cso_ansible_sdk.errors import BadRequestException
from cso_ansible_sdk.errors import ForbiddenException
from cso_ansible_sdk.errors import InternalServerErrorException
from cso_ansible_sdk.errors import MethodNotAllowedException
from cso_ansible_sdk.errors import NotAcceptableException
from cso_ansible_sdk.errors import NotFoundException
from cso_ansible_sdk.errors import ServiceUnavailableException
from cso_ansible_sdk.errors import TooManyRequestsException
from cso_ansible_sdk.errors import UnauthorizedException
from cso_ansible_sdk.errors import UnsupportedMediaTypeException


def error_report(function):
    def inner(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except HTTPError as e:
            if e.response.status_code == 400:
                raise BadRequestException(
                    "Malformatted requests: {}".format(e.response.text))
            elif e.response.status_code == 401:
                raise UnauthorizedException(
                    "Invalid credentials provided or account is locked: {}".format(
                        e.response.text))
            elif e.response.status_code == 403:
                raise ForbiddenException(
                    "Insufficient permissions to execute request (ie, any POST method as a regular user): {}".format(
                        e.response.text))
            elif e.response.status_code == 404:
                raise NotFoundException(
                    "Attempting to access an endpoint that does not exist: {}".format(
                        e.response.text))
            elif e.response.status_code == 405:
                raise MethodNotAllowedException(
                    "Wrong request type for target endpoint (ie, POSTing data to a GET endpoint): {}".format(
                        e.response.text))
            elif e.response.status_code == 406:
                raise NotAcceptableException(
                    "Content Type of the data returned does not match the Accept header of the request: {}".format(
                        e.response.text))
            elif e.response.status_code == 415:
                raise UnsupportedMediaTypeException(
                    "Attempting to POST data in incorrect format: {}".format(
                        e.response.text))
            elif e.response.status_code == 429:
                raise TooManyRequestsException(
                    "You have exceeded the max number of requests per 1-minute period: {}".format(
                        e.response.text))
            elif e.response.status_code == 500:
                raise InternalServerErrorException(
                    "Contact support if you see this error type: {}".format(
                        e.response.text))
            elif e.response.status_code == 503:
                raise ServiceUnavailableException(
                    "The ThousandEyes API is currently in maintenance mode: {}".format(
                        e.response.text))

    return inner
