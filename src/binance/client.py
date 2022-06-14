from typing import Tuple
from urllib.parse import urlencode

from src.utils.base_classes import ClientBase
from src.utils.schemas import BodyPrivateRequest


class ClientBinance(ClientBase):
    @staticmethod
    async def private_request(body: BodyPrivateRequest) -> Tuple:
        query_string = urlencode(body.payload)

