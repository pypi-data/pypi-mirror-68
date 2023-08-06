class BadRequestException(Exception):
    pass


class UnauthorizedException(Exception):
    pass


class ForbiddenException(Exception):
    pass


class NotFoundException(Exception):
    pass


class MethodNotAllowedException(Exception):
    pass


class NotAcceptableException(Exception):
    pass


class UnsupportedMediaTypeException(Exception):
    pass


class TooManyRequestsException(Exception):
    pass


class InternalServerErrorException(Exception):
    pass


class ServiceUnavailableException(Exception):
    pass
