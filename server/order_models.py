import asyncio
import random
from pydantic import BaseModel, field_validator
from enum import Enum, auto
from datetime import datetime

from server.misc import SUPPORTED_SYMBOLS
from server.database import ORDER_IDS
from server.exception_handlers import QuantityValidationError, SymbolValidationError, OrderNotFoundError


class CreateOrderRequest(BaseModel):
    symbol: str
    quantity: int

    @field_validator("symbol")
    def symbol_must_be_supported(cls, value):
        if value not in SUPPORTED_SYMBOLS:
            raise SymbolValidationError(f'Symbol: {str(value)} is not supported')
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
        self._created_time = datetime.now()

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
                                                                      'isoformat') else self._created_time
        }

    def __str__(self) -> str:
        return f"Order ID: {self.order_id}, Status: {self.status.name}, Stock: {self.symbol}, Quantity: {self.quantity}"

    async def execute_order(self):
        await asyncio.sleep(random.uniform(0.1, 2.0))
        self.update_status(OrderStatus.EXECUTED)
        return self.get_info()
