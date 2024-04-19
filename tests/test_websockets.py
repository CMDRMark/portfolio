import json
import pytest
from http import HTTPStatus
from aiohttp import ClientSession


@pytest.mark.asyncio
async def test_websocket_order_placed(ws_url, trading_api_client, delete_all_orders):

    async with ClientSession().ws_connect(url=ws_url) as ws_client:
        response = trading_api_client.place_order(quantity=10, symbol="EURUSD")
        assert response.status_code == HTTPStatus.CREATED
        async for message in ws_client:
            order_info = json.loads(message.data)
            assert order_info['order_id'] == response.json()['order_id']
            if order_info['status'] == "PENDING":
                await ws_client.close()
                break


@pytest.mark.asyncio
async def test_websocket_order_executed(ws_url, trading_api_client, delete_all_orders):

    async with ClientSession().ws_connect(url=ws_url) as ws_client:
        response = trading_api_client.place_order(quantity=10, symbol="EURUSD")
        assert response.status_code == HTTPStatus.CREATED
        async for message in ws_client:
            order_info = json.loads(message.data)
            assert order_info['order_id'] == response.json()['order_id']
            if order_info['status'] == "EXECUTED":
                await ws_client.close()
                break


@pytest.mark.asyncio
async def test_websocket_order_canceled(ws_url, trading_api_client, place_order_correct_and_get_id, delete_all_orders):
    async with ClientSession().ws_connect(url=ws_url) as ws_client:
        order_canceled = trading_api_client.delete_order(order_id=place_order_correct_and_get_id)
        assert order_canceled.status_code == HTTPStatus.OK
        async for message in ws_client:
            order_info = json.loads(message.data)
            assert order_info['order_id'] == order_canceled.json()['order_id']
            if order_info['status'] == "CANCELLED":
                await ws_client.close()
                break
