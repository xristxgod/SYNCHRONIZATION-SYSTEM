import hmac
import hashlib
from datetime import datetime
from typing import Union, Any

from src.types import API_SECRET_KEY


class Utils:
    @staticmethod
    def get_timestamp_now() -> int:
        return int(datetime.timestamp(datetime.now()))

    @staticmethod
    def convert_to_url(*args: str) -> str:
        return "".join(args)

    @staticmethod
    def hashing(query: str, secret_key: API_SECRET_KEY) -> str:
        return hmac.new(secret_key.encode("utf-8"), query.encode("utf-8"), hashlib.sha256).hexdigest()

    @staticmethod
    def get_one_month_ago() -> datetime:
        today = datetime.today()
        if today.month == 1:
            one_month_ago = today.replace(year=today.year - 1, month=12)
        else:
            extra_days = 0
            while True:
                try:
                    one_month_ago = today.replace(month=today.month - 1, day=today.day - extra_days)
                    break
                except ValueError:
                    extra_days += 1
        return one_month_ago

    @staticmethod
    def correct_parser_data(_type: Any, data: str = None) -> Union[Any, Exception]:
        """For run script"""
        if data is None:
            return None
        data = data.replace(" ", "")
        if _type == int and data.isdigit():
            return int(data)
        elif _type == list:
            if data.find(",") > 0:
                return list(filter(lambda x: x != "", data.split(",")))
            return [data]
        else:
            raise Exception("Something is wrong!")


utils = Utils
