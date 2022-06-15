from typing import Optional

from src.models import AccountModel
from src.types import API_NAME, API_KEY, API_SECRET_KEY
from src.inc.controller import account_controller
from src.inc.repositorys import keys_repository
from src.inc.schemas import RequestPrivateData, SetKeyData
from src.inc.controller import request_controller


class Account:
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

    if weight_used < 1000:
        response_headers, response_data = await request_controller.private(data=RequestPrivateData(

        ))
