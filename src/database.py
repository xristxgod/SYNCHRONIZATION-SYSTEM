import json
from typing import Optional, Union, List, Tuple, Dict, Any

import asyncpg

from src.utils.schemas import BodySetKey
from src.utils.types import API_NAME, API_KEY, API_SECRET_KEY
from config import Config


class KeysRepository:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(KeysRepository, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        # {"apiName": "hash-api-key-and-secret-key"}
        self.__api_keys = {"binance": {}, "bybit": {}}

    @staticmethod
    def encode(api_key: API_KEY, secret_key: API_SECRET_KEY) -> str:
        return json.dumps({api_key: secret_key}).encode("utf-8").hex()

    @staticmethod
    def decode(hash_string: str) -> Dict:
        return json.loads(bytes.fromhex(hash_string).decode("utf-8"))

    def set_key(self, network: str, body: BodySetKey) -> Union[bool, str]:
        if self.__api_keys[network].get(body.apiName) is None:
            self.__api_keys.get(network).update({
                body.apiName, KeysRepository.encode(api_key=body.apiKey, secret_key=body.secretKey)
            })
        else:
            return "This acc have in repository"
        return True

    def get_key(self, network: str, api_name: API_NAME) -> Tuple:
        if self.__api_keys[network].get(api_name) is not None:
            return list(KeysRepository.decode(self.__api_keys[network].get(api_name)).items())[0]
        return ()

    def del_key(self, network: str, api_name: API_NAME) -> bool:
        if self.__api_keys[network].get(api_name) is not None:
            self.__api_keys.get(network).pop(api_name)
        return True


class DB:
    @staticmethod
    async def _select_method(sql: str, data: Optional[Union[List, Tuple]] = ()):
        try:
            with await asyncpg.connect(Config.DATABASE_URL) as connection:
                return await connection.fetch(sql, data)
        except Exception as error:
            raise error

    @staticmethod
    async def _insert_method(sql: str, data: Optional[Union[List, Tuple]] = ()) -> bool:
        try:
            with await asyncpg.connect(Config.DATABASE_URL) as connection:
                await connection.execute(sql, data)
                await connection.commit()
            return True
        except Exception as error:
            raise error

    @staticmethod
    async def delete_all_orders(api_id: int, user_id: int) -> Optional:
        orders = await DB._select_method(
            "SELECT * FROM orders_model WHERE api_id = $1 AND user_id = $2;", (api_id, user_id)
        )
        if len(orders) > 0:
            await DB._insert_method(
                "DELETE FROM orders_model WHERE api_id = $1 AND user_id = $2;", (api_id, user_id)
            )

    @staticmethod
    async def create_order(api_id: int, user_id: int, order_data: Tuple[Any, ...]) -> Optional:
        orig_qty, price, side, position_side, status, symbol, time, ord_type = order_data
        await DB._insert_method(
            (
                "INSERT (orig_qty, price, side, position_side, status, symbol, time, ord_type, api_id, user_id) "
                "FROM orders_model VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10);"
            ),
            (
                orig_qty, price, side, position_side, status, symbol, time, ord_type, api_id, user_id
            )
        )

    @staticmethod
    async def get_account_info(api_id: int, user_id: int):
        return await DB._select_method(
            "SELECT * FROM account_model WHERE api_id = $1 AND user_id = $2;", (api_id, user_id)
        )


db = DB
keys_repository = KeysRepository()
