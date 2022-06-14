from typing import Optional

from src.binance.client import client_binance
from src.utils.schemas import BodyPrivateRequest
from src.utils.types import API_NAME


async def scrape(api_name: API_NAME) -> Optional:
    up_to_data, weight_used, processed, updated_positions, new_positions, updated_orders, sleep = False, 0, 0, 0, 0, 0, 0

    if weight_used < 1000:
        response_json, response_header = await client_binance.private_request(body=BodyPrivateRequest(
            apiName=api_name, httpMethod="GET", urlPath="/fapi/v1/openOrders"
        ))
        weight_used = int(response_header["X-MBX-USED-WEIGHT-1M"])
