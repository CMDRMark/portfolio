from http import HTTPStatus


def test_place_order(trading_api_client, delete_all_orders):
    response = trading_api_client.place_order(quantity=10, symbol="EURUSD")
    assert response.status_code == HTTPStatus.CREATED


def test_place_order_with_unsupported_symbol(trading_api_client):
    response = trading_api_client.place_order(quantity=10, symbol="EURUSDD")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()['detail'] == "Symbol: EURUSDD is not supported"


def test_place_order_with_incorrect_symbol_type(trading_api_client):
    response = trading_api_client.place_order(quantity=10, symbol=123)
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()['detail'] == "Input should be a valid string"


def test_place_order_with_negative_quantity(trading_api_client):
    response = trading_api_client.place_order(quantity=-10, symbol="EURUSD")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()['detail'] == "Quantity must be greater than zero"


def test_place_order_with_incorrect_quantity_type(trading_api_client):
    response = trading_api_client.place_order(quantity="10.12", symbol="EURUSD")
    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert response.json()['detail'] == "Quantity must be an integer"


def test_get_order_by_id(trading_api_client, place_order_correct_and_get_id):
    order_id = place_order_correct_and_get_id
    response = trading_api_client.get_order_by_id(order_id=order_id)
    assert response.status_code == HTTPStatus.OK
    assert order_id == response.json()['order_id']


def test_get_order_by_incorrect_id(trading_api_client):
    incorrect_order_id = 999999
    response = trading_api_client.get_order_by_id(order_id=incorrect_order_id)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == f"Order with ID: {incorrect_order_id} does not exist"


def test_get_all_orders(trading_api_client, place_order_correct_and_get_id):
    order_id = place_order_correct_and_get_id
    response = trading_api_client.get_orders()
    assert response.status_code == HTTPStatus.OK
    assert order_id in [x['order_id'] for x in response.json()]


def test_delete_order(trading_api_client, place_order_correct_and_get_id):
    order_id = place_order_correct_and_get_id
    response = trading_api_client.delete_order(order_id=order_id)
    assert response.status_code == HTTPStatus.OK


def test_delete_order_with_incorrect_id(trading_api_client):
    incorrect_order_id = 999999
    response = trading_api_client.delete_order(order_id=incorrect_order_id)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == f"Order with ID: {incorrect_order_id} does not exist"


def test_delete_executed_order(trading_api_client, place_order_wait_for_execution_and_get_id):
    order_id = place_order_wait_for_execution_and_get_id
    response = trading_api_client.delete_order(order_id=order_id)

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == f"Order with ID: {order_id} has already been executed"
