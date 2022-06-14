from typing import Optional, Dict
from dataclasses import dataclass

from src.utils.types import API_NAME, API_KEY, API_SECRET_KEY


# <<<=====================================>>> Client <<<=============================================================>>>


@dataclass
class BodyPublicRequest:
    httpMethod: str                                 # Http method. External: GET, POST
    urlPath: str                                    # Binance/ByBit Method url
    payload: Optional[Dict] = None                  # Payload


@dataclass
class BodyPrivateRequest:
    apiName: API_NAME                               # Api name in db
    httpMethod: str                                 # Http method. External: GET, POST
    urlPath: str                                    # Binance/ByBit Method url
    __payload: Optional[Dict] = None                # Payload

    @property
    def payload(self) -> Dict:
        if self.__payload is None:
            return {}
        return self.__payload


# <<<=====================================>>> Repository <<<=========================================================>>>


class BodySetKey:
    apiName: API_NAME                               # Api name in db
    apiKey: API_KEY                                 # Api key
    secretKey: API_SECRET_KEY                       # Api secrey key
