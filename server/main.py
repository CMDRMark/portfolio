import asyncio
import logging
import os
import random

from typing import List, Union
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, BackgroundTasks, status
from fastapi.exceptions import RequestValidationError, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from order_models import Order, CreateOrderRequest, OrderStatus
from exception_handlers import (validation_exception_handler, quantity_validation_exception_handler,
                                symbol_validation_exception_handler, quantity_type_validation_exception_handler,
                                order_not_found_exception_handler, QuantityValidationError, SymbolValidationError,
                                OrderNotFoundError, QuantityTypeValidationError, )

from database import DB, ORDER_IDS

app = FastAPI()
clients: List[WebSocket] = []

# Custom error handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(SymbolValidationError, symbol_validation_exception_handler)
app.add_exception_handler(QuantityValidationError, quantity_validation_exception_handler)
app.add_exception_handler(OrderNotFoundError, order_not_found_exception_handler)
app.add_exception_handler(QuantityTypeValidationError, quantity_type_validation_exception_handler)

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
    await broadcast_message(new_order.get_info())
    background_tasks.add_task(process_order, new_order)
    DB[str(new_id)] = new_order

    return JSONResponse(status_code=status.HTTP_201_CREATED,
                        content=new_order.get_info())


@app.get("/orders/{order_id}")
async def get_order(order_id: str) -> JSONResponse:
    await asyncio.sleep(random.uniform(0.1, 1))
    if int(order_id) not in ORDER_IDS and int(order_id) != 0:
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"detail": f"Order with ID: {order_id} does not exist"})
    return JSONResponse(status_code=status.HTTP_200_OK,
                        content=DB[order_id].get_info())


@app.delete("/orders/{order_id}")
async def delete_order(order_id: str) -> JSONResponse:
    await asyncio.sleep(random.uniform(0.1, 1))
    order = DB.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail=f"Order with ID: {order_id} does not exist")
    if order.status == order.status.EXECUTED:
        raise HTTPException(status_code=400, detail=f"Order with ID: {order_id} has already been executed")
    elif order.status == order.status.PENDING:
        DB[order_id].update_status(OrderStatus.CANCELLED)
        await broadcast_message(order.get_info())
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content=order.get_info())
    elif order.status == order.status.CANCELLED:
        raise HTTPException(status_code=400, detail=f"Order with ID: {order_id} has already been canceled")


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
        pass
    finally:
        clients.remove(websocket)


async def broadcast_message(message: dict):
    for client in clients:
        await client.send_json(message)


async def process_order(order: Order):
    order_info = await order.execute_order()
    await broadcast_message(order_info) if order_info else None


if __name__ == "__main__":
    import uvicorn
    from urllib.parse import urlparse

    inside_docker = os.getenv("INSIDE_DOCKER")
    logging.info(f"INSIDE_DOCKER: {inside_docker}")
    if not inside_docker:
        import dotenv
        dotenv.load_dotenv()
        logging.info("Loaded .env file")

    parsed_url = urlparse(os.getenv("BASE_URL"))
    hostname = parsed_url.hostname if not inside_docker else "0.0.0.0"

    port = parsed_url.port
    logging.info(f"Starting server at {hostname}:{port}")

    uvicorn.run(app, host=hostname, port=port)
