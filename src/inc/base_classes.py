from typing import Tuple
from src.utils.schemas import BodyPublicRequest, BodyPrivateRequest


class ClientBase:
    @staticmethod
    async def private_request(body: BodyPrivateRequest) -> Tuple:
        raise NotImplementedError

    @staticmethod
    async def public_request(body: BodyPublicRequest) -> Tuple:
        raise NotImplementedError

