# Trading API

This project is a mock REST API trading server built with Python and FastAPI. It allows users to place, get, and delete orders. It also supports WebSocket connections for real-time updates on order status.
Server is asynchronous. It uses pydantic for data validation and asynchronous random delays for request processing and order execution.

## Features

- Place an order
- Get an order by ID
- Get all orders
- Delete an order
- WebSocket support for real-time updates

## Easy launch with Docker

You can launch server and tests with docker-compose. 
Just run `docker-compose build` and `docker-compose up --abort-on-container-exit` in the root directory of the project.
Once tests are finished, you will see test report in the tests/ folder named `report.html`.


## Local Server Setup

1. Clone the repository
2. Create a virtual environment with `python -m venv venv`
3. Activate the virtual environment with `source venv/bin/activate` on Linux/macOS or `venv\Scripts\activate` on Windows 
4. Install the dependencies with `pip install -r requirements.txt`
5. By default, server will be launched on http://127.0.0.1:8000. You can change it in `.env` file by editing "BASE_URL" value. Same value is used in tests. If tests and server are launched inside docker, base urls will be changes to ensure connectivity between containers. 
6. Run the server with `python server/main.py`

## Server functionality

### HTTP API

The HTTP API supports the following endpoints:

You can check the api documentation by visiting `http://127.0.0.1:8000/docs` or whatever base url you have set in `.env` file.

- `POST /orders`: Place an order
- `GET /orders/{order_id}`: Get an order by ID
- `GET /orders`: Get all orders
- `DELETE /orders/{order_id}`: Delete an order

### WebSocket API

The WebSocket API sends real-time updates on order status. Connect to the WebSocket server at `ws://127.0.0.1:8000/ws`.

## Functional Tests

Tests are located in the `tests` directory. Run them with 
`pytest tests/.`.

Tests check for the following:

- Test Place Order: This test checks if an order can be placed successfully. It expects a status code of 201 (Created) when an order is placed with a quantity of 10 and the symbol "EURUSD".  
- Test Place Order with Unsupported Symbol: This test checks the response when an order is placed with an unsupported symbol. It expects a status code of 422 (Unprocessable Entity) and an error message stating that the symbol is not supported.  
- Test Place Order with Incorrect Symbol Type: This test checks the response when an order is placed with an incorrect symbol type. It expects a status code of 422 (Unprocessable Entity) and an error message stating that the input should be a valid string.  
- Test Place Order with Negative Quantity: This test checks the response when an order is placed with a negative quantity. It expects a status code of 422 (Unprocessable Entity) and an error message stating that the quantity must be greater than zero.  
- Test Place Order with Incorrect Quantity Type: This test checks the response when an order is placed with an incorrect quantity type. It expects a status code of 422 (Unprocessable Entity) and an error message stating that the quantity must be an integer.  
- Test Get Order by ID: This test checks if an order can be retrieved by its ID. It expects a status code of 200 (OK) and the order ID in the response.  
- Test Get Order by Incorrect ID: This test checks the response when trying to retrieve an order by an incorrect ID. It expects a status code of 404 (Not Found) and an error message stating that the order does not exist.  
- Test Get All Orders: This test checks if all orders can be retrieved. It expects a status code of 200 (OK) and the order ID in the list of orders.  
- Test Delete Order: This test checks if an order can be deleted. It expects a status code of 200 (OK) when an order is deleted.  
- Test Delete Order with Incorrect ID: This test checks the response when trying to delete an order with an incorrect ID. It expects a status code of 404 (Not Found) and an error message stating that the order does not exist.  
- Test Delete Executed Order: This test checks the response when trying to delete an executed order. It expects a status code of 400 (Bad Request) and an error message stating that the order has already been executed.
- Test WebSocket Update on Order Placement: This test checks if the WebSocket server sends an update when an order is placed. It expects a message with the order ID and status "Placed".
- Test WebSocket Update on Order Execution: This test checks if the WebSocket server sends an update when an order is executed. It expects a message with the order ID and status "Executed".
- Test WebSocket Update on Order Cancellation: This test checks if the WebSocket server sends an update when an order is deleted. It expects a message with the order ID and status "Canceled".

After test execution, you will see a test report in the `tests` directory named `report.html`.
You can check the report example here: [etc/report.html](https://html-preview.github.io/?url=https://github.com/CMDRMark/portfolio/blob/main/etc/report.html&sort=result)


## Performance Tests

For performance tests, I used k6 framework for its ability to generate big load.
Performance test script is located in the `performance` directory.
To run performance tests, you need to have k6 installed on your machine.

## Installing k6

You can download the latest version of k6 from the [releases page](https://k6.io/docs/get-started/installation/#download-the-k6-binary)
You can check more detailed instructions [here](https://k6.io/docs/get-started/installation/)

### macOS

You can install k6 on macOS using Homebrew:

1. If you don't have Homebrew installed, install it by running the following command in your terminal:

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

2. Once Homebrew is installed, you can install k6 with:

    ```bash
    brew install k6
    ```

### Windows

On Windows, you can install k6 using Chocolatey:

1. If you don't have Chocolatey installed, install it by running the following command in your PowerShell as an administrator:

    ```powershell
    Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
    ```

2. Once Chocolatey is installed, you can install k6 with:

    ```powershell
    choco install k6
    ```

After installation, you can verify that k6 is installed correctly by running:

```bash
k6 version 
```


## Performance Test Launch

Test Order Placement: Place orders for 1 minute with 100 VUs

Before running the test, make sure that the server is running, and the url in the test file is correct.

To run this test, use the following command:

```bash
K6_WEB_DASHBOARD=true K6_WEB_DASHBOARD_EXPORT=performance/performance-html-report.html K6_WEB_DASHBOARD_PERIOD=3s K6_WEB_DASHBOARD_OPEN=true k6 run performance/performance_test.js
```
On the test launch it will open a browser window with real-time test results with the result refresh rate every 3 seconds.

After test execution you will see a test report in the `performance` directory named `performance-html-report.html`.
You can check the report example [etc/performance-html-report.html](https://html-preview.github.io/?url=https://github.com/CMDRMark/portfolio/blob/main/etc/performance-html-report.html)

More info about test launch options can be found [here](https://grafana.com/docs/k6/latest/results-output/web-dashboard/)

## License

[MIT](https://choosealicense.com/licenses/mit/)
