import decimal
from typing import Optional, Tuple, Dict
from dataclasses import dataclass

from src.types import API_NAME, API_SECRET_KEY, API_KEY
from src.inc.base_classes import ToJson, FullJSON


# <<<==========================================>>> Repository classes type <<<=======================================>>>


@dataclass
class SetKeyData:
    apiName: API_NAME                               # Api name in db
    apiKey: API_KEY                                 # Api key
    secretKey: API_SECRET_KEY                       # Api secret key


# <<<==========================================>>> Database classes controller type <<<==============================>>>


@dataclass
class CreateOrderData(ToJson):
    """Create new order"""
    origQty: float
    price: decimal.Decimal
    side: str
    positionSide: str
    status: str
    symbol: str
    time: int
    api_name: API_NAME
    user_id: int

    @property
    def to_json(self) -> Dict:
        return self.__dict__


@dataclass
class UpdateAccountData(ToJson):
    """Update account information"""
    totalWalletBalance: decimal.Decimal
    totalUnrealizedProfit: decimal.Decimal
    totalMarginBalance: decimal.Decimal
    availableBalance: decimal.Decimal
    maxWithdrawAmount: decimal.Decimal
    api_name: API_NAME

    @property
    def to_json(self) -> Dict:
        data = self.__dict__
        if self.api_name is not None or self.api_name:
            data.pop("api_name")
        return data


@dataclass
class CreateIncomeData(ToJson):
    tranId: int
    symbol: str
    incomeType: str
    income: decimal.Decimal
    asset: str
    info: str
    time: int
    tradeId: int
    api_name: API_NAME
    user_id: int

    @property
    def to_json(self) -> Dict:
        return self.__dict__


@dataclass
class CUPositionData(ToJson, FullJSON):
    symbol: str
    unrealizedProfit: decimal.Decimal
    leverage: int
    liquidationPrice: decimal.Decimal
    entryPrice: decimal.Decimal
    positionSide: str
    positionAmt: decimal.Decimal
    api_name: API_NAME
    user_id: int

    @property
    def to_json(self) -> Dict:
        data = self.__dict__
        if self.api_name:
            data.pop("api_name")
        if self.user_id:
            data.pop("user_id")
        return data

    @property
    def full_json(self):
        return self.__dict__


# <<<==========================================>>> Request classes controller type <<<===============================>>>


@dataclass
class RequestPrivateData(ToJson):
    apiData: Tuple[API_KEY, API_SECRET_KEY]                   # (api_key, secret_key)
    httpMethod: str
    urlPath: str
    __payload: Optional[Dict]

    @property
    def payload(self) -> Dict:
        if self.__payload is None:
            return {}
        return self.__payload

    @property
    def to_json(self) -> Dict:
        if self.__payload is None:
            self.__payload = {}
        return self.__dict__


@dataclass
class RequestPublicData(ToJson):
    urlPath: str
    __payload: Optional[Dict]

    @property
    def payload(self) -> Dict:
        if self.__payload is None:
            return {}
        return self.__payload

    @property
    def to_json(self) -> Dict:
        if self.__payload is None:
            self.__payload = {}
        return self.__dict__
