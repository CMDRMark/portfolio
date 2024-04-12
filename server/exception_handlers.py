from urllib.request import Request

from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    errors = [e['msg'] for e in exc.errors()]
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


async def quantity_validation_exception_handler(request: Request, exc: QuantityValidationError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": exc.message})


class OrderNotFoundError(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


async def order_not_found_exception_handler(request: Request, exc: OrderNotFoundError) -> JSONResponse:
    return JSONResponse(status_code=422, content={"detail": exc.message})
