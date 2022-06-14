from typing import Tuple, Callable, Any
from urllib.parse import urlencode

import aiohttp

from src.database import keys_repository
from src.inc.exception import HTTPRequestError
from src.utils.utils import utils
from src.inc.base_classes import ClientBase
from src.utils.schemas import BodyPrivateRequest
from src.utils.types import API_KEY


class ClientBinance(ClientBase):
    BINANCE_URL = "binance_url"

    @staticmethod
    def _generate_url(*args: Any) -> str:
        return "".join(*args)

    @staticmethod
    async def _dispatch_request(method: str, api_key: API_KEY) -> Callable:
        session = aiohttp.ClientSession()
        session.headers.update({
            "Content-Type": "application/json;charset=utf-8",
            "X-MBX-APIKEY": api_key
        })
        return {
            "GET": session.get, "DELETE": session.delete, "PUT": session.put, "POST": session.post
        }.get(method, "GET")

    @staticmethod
    async def private_request(body: BodyPrivateRequest) -> Tuple:
        query_string = urlencode(body.payload).replace("%27", "%22")
        api_key, secret_key = keys_repository.get_key()
        if query_string:
            query_string = f"{query_string}&timestamp={utils.get_timestamp()}"
        else:
            query_string = f"timestamp={utils.get_timestamp()}"

        url = ClientBinance._generate_url(
            ClientBinance.BINANCE_URL, body.urlPath, "&", query_string,
            "&signature=", utils.hashing(query_string, secret_key)
        )
        params = {"url": url, "params": {}}
        response = (await ClientBinance._dispatch_request(api_key=api_key, method=body.httpMethod))(**params)
        headers = response.headers
        json_response = await response.json()
        if "code" in json_response:
            raise HTTPRequestError(url=url, code=json_response.get("code"), msg=json_response.get("msg"))
        return headers, json_response



