import time
import hmac
import hashlib

from src.utils.types import API_SECRET_KEY


class Utils:
    @staticmethod
    def get_timestamp() -> int:
        return int(time.time() * 1000)

    @staticmethod
    def hashing(query_string: str, secret_key: API_SECRET_KEY) -> str:
        return hmac.new(secret_key.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()


utils = Utils
