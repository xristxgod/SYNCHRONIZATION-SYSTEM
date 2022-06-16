import time
import datetime
from typing import Optional

from src.models import AccountModel
from src.types import API_NAME, API_KEY, API_SECRET_KEY
from src.inc.controller import account_controller, order_controller, position_controller, income_controller
from src.inc.repositorys import keys_repository
from src.inc.schemas import (
    CreateOrderData, CUPositionData, CreateIncomeData, UpdateAccountData,
    RequestPrivateData, SetKeyData
)
from src.inc.controller import request_controller
from src.utils.utils import utils
from config import decimals, logger


class AccountRepository:
    """Account"""
    def __init__(self, api_name: API_NAME, user_id: int):
        self.api_name: API_NAME = api_name
        self.user_id = user_id

        self.__api_key: API_KEY = None
        self.__secret_key: API_SECRET_KEY = None

    @property
    def api_key(self) -> str:
        if self.__api_key:
            return self.__api_key
        self.set_settings()
        return self.__api_key

    @api_key.setter
    def api_key(self, key: API_KEY):
        self.__api_key = key

    @property
    def secret_key(self) -> str:
        if self.__secret_key:
            return self.__secret_key
        self.set_settings()
        return self.__secret_key

    @secret_key.setter
    def secret_key(self, key: API_SECRET_KEY):
        self.__secret_key = key

    def set_settings(self) -> Optional:
        """Set api key and secret key"""
        api_key, secret_key = keys_repository.get_key(api_name=self.api_name)
        if not api_key and not secret_key:
            account_data = await account_controller.read(api_name=self.api_name)
            api_key, secret_key = account_data.api_key, account_data.secret_key
            if account_data is not None:
                keys_repository.set_key(network="binance", data=SetKeyData(
                    apiName=self.api_name, apiKey=api_key, secretKey=secret_key
                ))
        self.api_key, self.secret_key = api_key, secret_key
        return


def scrape(api_name: str, user_id: int):
    time_start = time.time()
    up_to_date = False
    weight_used, sleeps, processed, updated_positions, new_positions, updated_orders = 0, 0, 0, 0, 0, 0
    account = AccountRepository(api_name=api_name, user_id=user_id)
    if weight_used < 1000:
        response_headers, response_data = await request_controller.private(data=RequestPrivateData(
            apiData=(account.api_key, account.secret_key), httpMethod="GET", urlPath="/fapi/v1/openOrders"
        ))
        weight_used = int(response_headers["X-MBX-USED-WEIGHT-1M"])
        await order_controller.delete(api_name=account.api_name, user_id=account.user_id)
        for order in response_data:
            updated_orders += 1
            order_controller.create(data=CreateOrderData(
                origQty=float(order["origQty"]), price=decimals.create_decimal(order["price"]), side=order["side"],
                positionSide=order["positionSide"], status=order["status"], symbol=order["symbol"],
                time=int(order["time"]), type=order["type"], api_name=account.api_name, user_id=account.user_id
            ))
    response_headers, response_data = await request_controller.private(data=RequestPrivateData(
        apiData=(account.api_key, account.secret_key), httpMethod="GET", urlPath="/fapi/v2/account"
    ))
    weight_used = int(response_headers["X-MBX-USED-WEIGHT-1M"])
    if "positions" not in response_data:
        await account_controller.update(data=UpdateAccountData(
            api_name=account.api_name,
            totalWalletBalance=decimals.create_decimal(response_data["totalWalletBalance"]),
            totalUnrealizedProfit=decimals.create_decimal(response_data["totalUnrealizedProfit"]),
            totalMarginBalance=decimals.create_decimal(response_data["totalMarginBalance"]),
            availableBalance=decimals.create_decimal(response_data["availableBalance"]),
            maxWithdrawAmount=decimals.create_decimal(response_data["maxWithdrawAmount"])
        ))
        await position_controller.delete(api_name=account.api_name, user_id=account.user_id)
        positions = [*filter(lambda x: float(x["positionAmt"]) != 0, response_data["positions"])]

        for position in positions:
            liquidation_price = decimals.create_decimal(0)
            data_positions_risk = RequestPrivateData(
                apiData=(account.api_key, account.secret_key), httpMethod="GET", urlPath="/fapi/v2/account"
            )
            data_positions_risk.payload = {"symbol": position["symbol"]}
            _, positions_risk_response = await request_controller.private(data=data_positions_risk)
            if isinstance(positions_risk_response, list) and len(positions_risk_response) > 0:
                for positions_risk in positions_risk_response:
                    if positions_risk.get("positionSide") == position["positionSide"]:
                        liquidation_price = decimals.create_decimal(positions_risk.get("liquidationPrice"))
                        break
            data = CUPositionData(
                unrealizedProfit=decimals.create_decimal(position["unrealizedProfit"]),
                leverage=int(position["leverage"]),
                liquidationPrice=liquidation_price,
                entryPrice=decimals.create_decimal(position["entryPrice"]),
                positionAmt=decimals.create_decimal(position["positionAmt"]),
                symbol=position["symbol"],
                positionSide=position["positionSide"],
                api_name=account.api_name,
                user_id=account.user_id
            )
            position_check = await position_controller.read(
                api_name=account.api_name, user_id=account.user_id,
                symbol=position["symbol"], positionSide=position["positionSide"]
            )
            if position_check is None:
                await position_controller.create(data=data)
                new_positions += 1
            elif decimals.create_decimal(position_check.unrealizedProfit) != decimals.create_decimal(position["unrealizedProfit"]):
                await position_controller.update(data=data)
                updated_positions += 1

    while not up_to_date:
        if weight_used > 1100:
            logger.error(f"WEIGHT USED: {weight_used}\nPROCESSED: {processed}\nSKIPPING FOR NEXT TIME")
            break

        income_check = await income_controller.read(api_name=account.api_name, user_id=account.user_id)
        if income_check is None:
            one_month_ago = utils.get_one_month_ago()
            start_time = int(one_month_ago.timestamp() * 1000)
        else:
            start_time = income_check.time
        params = {"startTime": start_time + 1, "limit": 1000}
        data = RequestPrivateData(
            apiData=(account.api_key, account.secret_key), httpMethod="GET", urlPath="/fapi/v1/income",
        )
        data.payload = params
        response_headers, response_data = await request_controller.private(data=data)
        weight_used = int(response_headers["X-MBX-USED-WEIGHT-1M"])

        if len(response_data) == 0:
            up_to_date = True
        else:
            for income in response_data:
                if len(income["tradeId"]) == 0:
                    income["tradeId"] = 0
                await income_controller.create(data=CreateIncomeData(
                    tranId=int(income["tranId"]), symbol=income["symbol"], incomeType=income["incomeType"],
                    income=decimals.create_decimal(income["income"]), asset=income["asset"], info=income["info"],
                    time=int(income["time"]), tradeId=int(income["tradeId"]),
                    api_name=account.api_name, user_id=account.user_id
                ))
                processed += 1
        logger.error((
            f"ORDER UPDATE: {updated_orders}\n"
            f"POSITION UPDATE: {updated_positions} (new: {new_positions})\n"
            f"TRADES PROCESSED: {processed}\n"
            f"TIME ELAPSED: {datetime.timedelta(seconds=time.time() - start_time)}\n"
            f"SLEEP: {sleeps}"
        ))
