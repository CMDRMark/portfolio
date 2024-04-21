import asyncio
import random
from pydantic import BaseModel, field_validator
from enum import Enum, auto
from datetime import datetime
from typing import Any

from misc import SUPPORTED_SYMBOLS
from exception_handlers import QuantityValidationError, SymbolValidationError, QuantityTypeValidationError


class CreateOrderRequest(BaseModel):
    symbol: str
    quantity: Any  # Set to Any to allow for validation to be done in the field_validator with custom error messages

    @field_validator("symbol")
    def symbol_must_be_supported(cls, value):
        if value not in SUPPORTED_SYMBOLS:
            raise SymbolValidationError(f'Symbol: {str(value)} is not supported')
        return value

    @field_validator("quantity")
    def quantity_must_be_integer(cls, value):
        if not isinstance(value, int):
            msg = ''
            if isinstance(value, float):
                msg = 'Quantity should be a valid integer, got a number with a fractional part'
            elif isinstance(value, str):
                msg = 'Quantity must be an integer'
            raise QuantityTypeValidationError(msg)
        return value

    @field_validator("quantity")
    def quantity_must_be_positive(cls, value):
        if value <= 0:
            raise QuantityValidationError('Quantity must be greater than zero')
        return value


class OrderStatus(Enum):
    PENDING = auto()
    EXECUTED = auto()
    CANCELLED = auto()


class Order:
    def __init__(self, order_id: int, symbol: str, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero")
        self._order_id = order_id
        self._status = OrderStatus.PENDING
        self._symbol = symbol
        self._quantity = quantity
        self._created_time = datetime.now().timestamp()
        self._executed_time = None

    @property
    def status(self) -> OrderStatus:
        return self._status

    @property
    def order_id(self) -> str:
        return str(self._order_id)

    @property
    def symbol(self) -> str:
        return self._symbol

    @property
    def quantity(self) -> int:
        return self._quantity

    def update_status(self, new_status: OrderStatus):
        if not isinstance(new_status, OrderStatus):
            raise ValueError("Invalid status type")
        self._status = new_status

    def get_info(self):
        return {
            "order_id": self._order_id,
            "status": self._status.name,  # Assuming status is an enum
            "symbol": self._symbol,
            "quantity": self._quantity,
            "created_time": self._created_time.isoformat() if hasattr(self._created_time,
                                                                      'isoformat') else self._created_time,
            "executed_time": self._executed_time.isoformat() if hasattr(self._executed_time,
                                                                        'isoformat') else self._executed_time
        }

    def __str__(self) -> str:
        return f"Order ID: {self.order_id}, Status: {self.status.name}, Stock: {self.symbol}, Quantity: {self.quantity}"

    async def execute_order(self):
        await asyncio.sleep(random.uniform(4, 6.0))
        if self.status == OrderStatus.PENDING:
            self.update_status(OrderStatus.EXECUTED)
            self._executed_time = datetime.now().timestamp()
            return self.get_info()
