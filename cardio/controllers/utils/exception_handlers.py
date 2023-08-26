from fastapi import Request, status
from fastapi.responses import JSONResponse
from loguru import logger

from cardio.controllers.utils.models import Error
from cardio.services.errors import NotFoundError, BadRequestError, InternalError

def not_found_handler(request: Request, exc: NotFoundError):
    logger.info(f'NotFoundError: {exc}')
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=Error(message=str(exc)).model_dump(),
    )

def bad_request_handler(request: Request, exc: BadRequestError):
    logger.info(f'BadRequestError: {exc}')
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=Error(message=str(exc)).model_dump(),
    )

def internal_server_error_handler(request: Request, exc: InternalError):
    logger.error(f'InternalError: {exc}')
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=Error(message=str(exc)).model_dump(),
    )
