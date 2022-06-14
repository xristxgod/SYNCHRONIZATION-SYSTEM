from typing import Optional, Tuple

from src.binance.client import client_binance
from src.database import db
from src.utils.schemas import BodyPrivateRequest
from src.utils.types import API_NAME


async def scrape(user_id: int, api_data: Tuple[int, API_NAME]) -> Optional:
    up_to_data, weight_used, processed, updated_positions, new_positions, updated_orders, sleep = False, 0, 0, 0, 0, 0, 0

    if weight_used < 1000:
        response_json, response_header = await client_binance.private_request(body=BodyPrivateRequest(
            apiName=api_data[1], httpMethod="GET", urlPath="/fapi/v1/openOrders"
        ))
        weight_used = int(response_header["X-MBX-USED-WEIGHT-1M"])
        await db.delete_all_orders(api_id=api_data[0], user_id=user_id)
        for order in response_header:
            updated_orders += 1
            row = (
                float(order.get("origQty")), float(order.get("price")), order.get("side"), order.get("positionSide"),
                order.get("status"), order.get("symbol"), int(order.get("time")), order.get("type")
            )
            await db.create_order(order_data=row, api_id=api_data[0], user_id=user_id)

    response_header, response_json = await client_binance.private_request(body=BodyPrivateRequest(
        apiName=api_data[1], httpMethod="GET", urlPath="/fapi/v2/account"
    ))
    weight_used = int(response_header["X-MBX-USED-WEIGHT-1M"])

    if response_json.get("positions") is None:
        total_row = (
            float(response_json.get('totalWalletBalance')), float(response_json.get('totalUnrealizedProfit')),
            float(response_json.get('totalMarginBalance')), float(response_json.get('availableBalance')),
            float(response_json.get('maxWithdrawAmount'))
        )
        account_check = db.get_account_info(api_id=api_data[0], user_id=user_id)
        if account_check.get(""):
            pass


