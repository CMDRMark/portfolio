from urllib.request import Request

from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = exc.errors()[0]['msg']
    return JSONResponse(status_code=422, content={"detail": errors})


class SymbolValidationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


async def symbol_validation_exception_handler(request: Request, exc: SymbolValidationError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": exc.message})


class QuantityValidationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class QuantityTypeValidationError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


async def quantity_type_validation_exception_handler(request: Request, exc: QuantityTypeValidationError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": exc.message})


async def quantity_validation_exception_handler(request: Request, exc: QuantityValidationError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": exc.message})


class OrderNotFoundError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


async def order_not_found_exception_handler(request: Request, exc: OrderNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": exc.message})
