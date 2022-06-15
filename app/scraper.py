from typing import Optional

from src.models import AccountModel
from src.types import API_NAME, API_KEY, API_SECRET_KEY
from src.inc.controller import account_controller, order_controller, position_controller
from src.inc.repositorys import keys_repository
from src.inc.schemas import CreateOrderData, CUPositionData, UpdateAccountData, RequestPrivateData, SetKeyData
from src.inc.controller import request_controller
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
            data = CUPositionData(
                unrealizedProfit=decimals.create_decimal(position["unrealizedProfit"]),
                leverage=int(position["leverage"]),
                liquidationPrice=0,
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
            pass


