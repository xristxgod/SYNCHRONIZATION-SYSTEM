import decimal
from typing import Optional, Dict
from dataclasses import dataclass

from src.inc.base_classes import ToJson


# <<<==========================================>>> Database classes controller type <<<==============================>>>

@dataclass
class CreateOrderData(ToJson):
    """Create new order"""
    origQty: float
    price: decimal.Decimal
    liquidationPrice: Optional[decimal.Decimal]
    side: str
    positionSide: str
    status: str
    symbol: str
    time: int
    api_name: str
    user_id: int

    @property
    def to_json(self) -> Dict:
        if self.liquidationPrice is None:
            self.liquidationPrice = decimal.Decimal(0)
        return self.__dict__


@dataclass
class UpdateAccountData(ToJson):
    """Update account information"""
    api_name: str
    totalWalletBalance: decimal.Decimal
    totalUnrealizedProfit: decimal.Decimal
    totalMarginBalance: decimal.Decimal
    availableBalance: decimal.Decimal
    maxWithdrawAmount: decimal.Decimal

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
    api_name: str
    user_id: int

    @property
    def to_json(self) -> Dict:
        return self.__dict__
