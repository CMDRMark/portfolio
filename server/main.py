import asyncio
import random

from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks, status
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from server.order_models import Order, CreateOrderRequest
from server.exception_handlers import (validation_exception_handler, quantity_validation_exception_handler,
                                       symbol_validation_exception_handler, QuantityValidationError,
                                       SymbolValidationError, OrderNotFoundError, order_not_found_exception_handler)

from server.database import DB, ORDER_IDS

app = FastAPI()
clients: List[WebSocket] = []

# Pydantic model validation error handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SymbolValidationError, symbol_validation_exception_handler)
app.add_exception_handler(QuantityValidationError, quantity_validation_exception_handler)
app.add_exception_handler(OrderNotFoundError, order_not_found_exception_handler)

# Middleware to resolve possible websocket origins conflicts
app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )


@app.post("/orders")
async def create_order(order: CreateOrderRequest, background_tasks: BackgroundTasks) -> JSONResponse:
    await asyncio.sleep(random.uniform(0.1, 1))
    ORDER_IDS.append(ORDER_IDS[-1] + 1)
    new_id = ORDER_IDS[-1]
    new_order = Order(order_id=new_id, symbol=order.symbol, quantity=order.quantity)
    await broadcast_message(str(new_order.get_info()))
    background_tasks.add_task(process_order, new_order)
    DB[str(new_id)] = new_order

    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=new_order.get_info())


@app.get("/orders/{order_id}")
async def get_order(order_id: str) -> JSONResponse:
    await asyncio.sleep(random.uniform(0.1, 1))
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=DB[order_id].get_info())


@app.delete("/orders/{order_id}")
async def delete_order(order_id: str) -> JSONResponse:
    await asyncio.sleep(random.uniform(0.1, 1))
    if order_id not in DB:
        raise HTTPException(status_code=404, detail=f"Order with ID: {order_id} does not exist")
    del DB[order_id]
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content={"message": f"Order with ID: {order_id} deleted"})


@app.get("/orders")
async def get_orders() -> JSONResponse:
    await asyncio.sleep(random.uniform(0.1, 1))
    orders = [order.get_info() for order in DB.values()]
    if orders:
        return JSONResponse(status_code=status.HTTP_200_OK, content=orders)

    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": "No orders found"})


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    clients.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        clients.remove(websocket)


async def broadcast_message(message: str):
    for client in clients:
        await client.send_text(message)


async def process_order(order: Order):
    order_info = await order.execute_order()
    await broadcast_message(str(order_info))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
