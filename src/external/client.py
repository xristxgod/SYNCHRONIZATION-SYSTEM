import aiohttp

from src.types import API_NAME


class Client:
    @staticmethod
    async def dispatch(method: str, api_key: API_NAME = None):
        session = aiohttp.ClientSession()
        session.headers.update({
            "Content-Type": "application/json;charset=utf-8",
            "X-MBX-APIKEY": api_key
        })
        return {
            "GET": session.get,
            "DELETE": session.delete,
            "PUT": session.put,
            "POST": session.post
        }.get(method, "GET")


client = Client
