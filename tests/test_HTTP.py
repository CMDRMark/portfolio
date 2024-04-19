import pytest
import json
from http import HTTPStatus


def test_place_order(trading_api_client, delete_all_orders):
    response = trading_api_client.place_order(quantity=10, symbol="EURUSD")
    assert response.status_code == HTTPStatus.CREATED


def test_get_order_by_id(trading_api_client, place_order_correct_and_get_id):
    order_id = place_order_correct_and_get_id
    response = trading_api_client.get_order_by_id(order_id=order_id)
    assert response.status_code == HTTPStatus.OK
    assert order_id == response.json()['order_id']


def test_get_all_orders(trading_api_client, place_order_correct_and_get_id):
    order_id = place_order_correct_and_get_id
    response = trading_api_client.get_orders()
    assert response.status_code == HTTPStatus.OK
    assert order_id in [x['order_id'] for x in response.json()]


def test_delete_order(trading_api_client, place_order_correct_and_get_id):
    order_id = place_order_correct_and_get_id
    response = trading_api_client.delete_order(order_id=order_id)
    assert response.status_code == HTTPStatus.OK
