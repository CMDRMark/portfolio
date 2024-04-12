import logging

import requests
import urllib3
from typing import Callable


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
urllib3_logger = logging.getLogger("urllib3")
urllib3_logger.setLevel(logging.ERROR)

logger = logging.getLogger(__name__)


def log_request_response_info(func: Callable):

    def wrapper(*args, **kwargs):
        response: requests.Response = func(*args, **kwargs)
        logger.debug(f"Request URL: {response.url}")
        logger.debug(f"Request Method: {response.request.method}")
        logger.debug(f"Request Headers: {response.request.headers}")
        logger.debug(f"Request Body: {response.request.body}")
        logger.debug(f"Response Status Code: {response.status_code}")
        logger.debug(f"Response Headers: {response.headers}")
        logger.debug(f"Response Body: {response.text}")

        return response

    return wrapper


@log_request_response_info
def get_request(url, headers=None, cookies=None, json=None, data=None, verify=False):
    return requests.get(url=url, headers=headers, cookies=cookies, json=json, data=data, verify=verify)


@log_request_response_info
def post_request(url, headers=None, cookies=None, json=None, data=None, verify=False):
    return requests.post(url=url, headers=headers, cookies=cookies, json=json, data=data, verify=verify)


@log_request_response_info
def delete_request(url, headers=None, cookies=None, json=None, data=None, verify=False):
    return requests.delete(url=url, headers=headers, cookies=cookies, json=json, data=data, verify=verify)


@log_request_response_info
def put_request(url, headers=None, cookies=None, json=None, data=None, verify=False):
    return requests.put(url=url, headers=headers, cookies=cookies, json=json, data=data, verify=verify)


@log_request_response_info
def options_request(url, headers=None, cookies=None, json=None, data=None, verify=False):
    return requests.options(url=url, headers=headers, cookies=cookies, json=json, data=data, verify=verify)
