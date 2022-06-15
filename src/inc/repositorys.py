import json
from typing import Union, Optional, Tuple, Dict

from src.inc.schemas import SetKeyData
from src.types import API_NAME, API_KEY, API_SECRET_KEY


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

    def set_key(self, network: str, data: SetKeyData) -> Union[bool, str]:
        if self.__api_keys[network].get(data.apiName) is None:
            self.__api_keys.get(network).update({
                data.apiName, KeysRepository.encode(api_key=data.apiKey, secret_key=data.secretKey)
            })
        else:
            return "This acc have in repository"
        return True

    def get_key(self, network: str, api_name: API_NAME) -> Tuple[Optional[str], Optional[str]]:
        if self.__api_keys[network].get(api_name) is not None:
            return list(KeysRepository.decode(self.__api_keys[network].get(api_name)).items())[0]
        return None, None

    def del_key(self, network: str, api_name: API_NAME) -> bool:
        if self.__api_keys[network].get(api_name) is not None:
            self.__api_keys.get(network).pop(api_name)
        return True


keys_repository = KeysRepository()
