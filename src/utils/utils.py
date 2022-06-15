import hmac
import hashlib
from datetime import datetime


class Utils:
    @staticmethod
    def get_timestamp_now() -> int:
        return int(datetime.timestamp(datetime.now()))

    @staticmethod
    def convert_to_url(*args: str) -> str:
        return "".join(args)

    @staticmethod
    def hashing(query: str, secret_key: str):
        return hmac.new(secret_key.encode("utf-8"), query.encode("utf-8"), hashlib.sha256).hexdigest()


utils = Utils
