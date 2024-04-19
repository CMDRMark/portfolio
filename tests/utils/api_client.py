from typing import Union

import requests

from tests.utils.custom_requests import post_request, get_request, delete_request, options_request
from dotenv import load_dotenv
import os


class TradingAPIClient:
    def __init__(self):
        load_dotenv()
        self.base_url = os.getenv("BASE_URL")
        self.create_order_url = f"{self.base_url}/orders"
        self.get_del_order = f"{self.base_url}/orders/ORDER_ID"
        self.ws_url = f"{self.base_url}/ws"

    def place_order(self, quantity: int, symbol: str) -> requests.Response:
        return post_request(url=self.create_order_url, json={"symbol": symbol, "quantity": quantity}, verify=False)

    def get_orders(self) -> requests.Response:
        return get_request(url=self.create_order_url, verify=False)

    def get_order_by_id(self, order_id: Union[int, str]) -> requests.Response:
        if isinstance(order_id, int):
            order_id = str(order_id)
        return get_request(url=self.get_del_order.replace("ORDER_ID", order_id))

    def delete_order(self, order_id: Union[int, str]) -> requests.Response:
        if isinstance(order_id, int):
            order_id = str(order_id)
        return delete_request(url=self.get_del_order.replace("ORDER_ID", order_id))
