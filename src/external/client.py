import aiohttp


class Client:
    @staticmethod
    async def dispatch(method: str, api_key: str = None):
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
