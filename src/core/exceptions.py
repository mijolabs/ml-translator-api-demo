from http import HTTPStatus

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError


class BaseError(Exception):
    http_status: HTTPStatus = HTTPStatus.INTERNAL_SERVER_ERROR

    def __init__(self, message: str | None = None, error_code: str | None = None) -> None:
        self.status_code: int = self.http_status.value
        self.message: str = message or self.http_status.phrase
        self.error_code: str = error_code or self.http_status.name
        super().__init__(self.status_code, self.message, self.error_code)


class BadRequestError(BaseError):
    http_status = HTTPStatus.BAD_REQUEST


class LanguageDetectionError(BaseError):
    http_status = HTTPStatus.UNPROCESSABLE_CONTENT
    message = "Unable to detect language with confidence."


class UnsupportedLanguagePairError(BaseError):
    http_status = HTTPStatus.NOT_IMPLEMENTED
    message = "Translation for the specified language pair is not supported."


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        _request: Request,
        _exc: RequestValidationError,
    ) -> None:
        raise BadRequestError
