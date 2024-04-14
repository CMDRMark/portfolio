import pytest
import logging
import urllib3


SUPPORTED_SYMBOLS = ["EURUSD", "USDEUR", "CADUSD", "USDCAD"]


@pytest.fixture(scope="session", autouse=True)
def disable_warnings():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    urllib3_logger = logging.getLogger("urllib3")
    urllib3_logger.setLevel(logging.ERROR)


