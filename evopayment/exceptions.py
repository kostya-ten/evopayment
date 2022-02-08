import logging
from typing import TypeVar, Union, Optional

from fastapi import Request, status
from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import ORJSONResponse
from pydantic import BaseModel, Field

ExceptionType = TypeVar('ExceptionType')

logger = logging.getLogger('evopayment')


class ModelException(BaseModel):
    message: str
    fields: Optional[dict[str, str]] = Field(None)


class MainException(HTTPException):
    def __init__(self, message: str, status_code: int):
        super().__init__(status_code=status_code, detail=message)
        self.status_code = status_code
        self.message = message


class JWTException(MainException):
    """ JWT  """

    def __init__(self, message: str = 'JWT error decode'):
        super().__init__(message=message, status_code=status.HTTP_403_FORBIDDEN)


class NotFoundException(MainException):
    """ Not found object """

    def __init__(self, message: str = 'Object not found'):
        super().__init__(message=message, status_code=status.HTTP_404_NOT_FOUND)


class UnauthorizedException(MainException):
    """ Bad Authentication Exception """

    def __init__(self, message: str = 'Unauthorized'):
        super().__init__(message=message, status_code=status.HTTP_401_UNAUTHORIZED)


class ConflictException(MainException):
    """ Object conflicts """

    def __init__(self, message: str = 'Object conflict'):
        super().__init__(message=message, status_code=status.HTTP_409_CONFLICT)


class RMQConnectionErrorException(MainException):
    """ Rabbit MQ connection error """
    def __init__(self, message: str = 'Rabbit MQ connection error'):
        super().__init__(message=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BadRequestException(MainException):
    """ Bad request error """
    def __init__(self, message: str = 'Bad Request'):
        super().__init__(message=message, status_code=status.HTTP_400_BAD_REQUEST)


class NotFoundIPAddressException(MainException):
    """ Not found headers x-real-ip """
    def __init__(self, message: str = 'Not found headers x-real-ip'):
        super().__init__(message=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RedisConnectionErrorException(MainException):
    """ Redis connection error """
    def __init__(self, message: str = 'Redis connection error'):
        super().__init__(message=message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


def exception(exc_type: ExceptionType):  # skipcq: PYL-W0613

    async def wrapper(
        request: Request,
        err: Union[
            NotFoundException,
            UnauthorizedException,
            ConflictException,
            JWTException,
            RMQConnectionErrorException,
            BadRequestException,
            NotFoundIPAddressException,
            RedisConnectionErrorException,
        ]
    ):
        if isinstance(err, RequestValidationError):
            fields = {}
            for error in err.errors():
                field = error['loc'][-1]
                fields[field] = error['msg']

            return ORJSONResponse(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                content=ModelException.parse_obj({
                    'message': 'Invalid fields',
                    'fields': fields,
                }).dict(),
            )
        else:
            return ORJSONResponse(
                status_code=err.status_code,
                content=ModelException.parse_obj({'message': err.message}).dict(exclude_none=True)
            )
    return wrapper


# Registering exceptions in FastAPI
exception_handlers = {
    RequestValidationError: exception(RequestValidationError),
    NotFoundException: exception(NotFoundException),
    UnauthorizedException: exception(UnauthorizedException),
    ConflictException: exception(ConflictException),
    JWTException: exception(JWTException),
    RMQConnectionErrorException: exception(RMQConnectionErrorException),
    BadRequestException: exception(BadRequestException),
    NotFoundIPAddressException: exception(NotFoundIPAddressException),
    RedisConnectionErrorException: exception(RedisConnectionErrorException),
}

exception_responses = {
    404: {'model': ModelException},
    403: {'model': ModelException},
    401: {'model': ModelException},
    409: {'model': ModelException},
    400: {'model': ModelException},
    422: {'model': ModelException},
    500: {'model': ModelException},
}
