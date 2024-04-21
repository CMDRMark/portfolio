import os
import time

import pytest
import logging
import urllib3


from tests.utils.api_client import TradingAPIClient

SUPPORTED_SYMBOLS = ["EURUSD", "USDEUR", "CADUSD", "USDCAD"]


@pytest.fixture(scope="session", autouse=True)
def setup_logging():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    urllib3_logger = logging.getLogger("urllib3")
    urllib3_logger.setLevel(logging.ERROR)
    aiohttp_logger = logging.getLogger('aiohttp')
    aiohttp_logger.setLevel(logging.DEBUG)


@pytest.fixture(scope="session")
def trading_api_client():
    client = TradingAPIClient()
    yield client


@pytest.fixture(scope="function")
def place_order_correct_and_get_id(trading_api_client):
    response = trading_api_client.place_order(symbol="EURUSD", quantity=4)
    return response.json()["order_id"]


@pytest.fixture(scope="function")
def place_order_wait_for_execution_and_get_id(trading_api_client):
    response = trading_api_client.place_order(symbol="EURUSD", quantity=4)
    if response.status_code != 201:
        logging.error(f"Failed to place order: {response.json()}")
    order_id = response.json()["order_id"]
    order_status = trading_api_client.get_order_by_id(order_id).json()["status"]
    while order_status != "EXECUTED":
        time.sleep(2)
        response = trading_api_client.get_order_by_id(order_id)
        if response.status_code != 200:
            logging.error(f"Failed to get order: {response.json()}")
        order_status = response.json()["status"]

    return order_id


@pytest.fixture(scope="function")
def delete_all_orders(trading_api_client):
    yield
    orders = trading_api_client.get_orders()
    orders = [x['order_id'] for x in orders.json() if x['status'] == "PENDING"]
    for order_id in orders:
        trading_api_client.delete_order(order_id=str(order_id))


@pytest.fixture(scope="function")
def ws_url():
    ws_url = os.getenv("BASE_URL").replace("http", "ws") + "/ws"
    return ws_url
