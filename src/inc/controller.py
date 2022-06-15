from typing import Optional

from tortoise.queryset import MODEL

from src.models import OrderModel, AccountModel, IncomeModel
from src.inc.base_classes import DBShow, DBCreate, DBUpdate, DBDelete
from src.inc.schemas import CreateOrderData, CreateIncomeData
from src.inc.schemas import UpdateAccountData
from config import logger


class OrderController(DBCreate, DBDelete):
    """Order controller | Add new order & delete ALL order"""
    @staticmethod
    async def create(data: CreateOrderData) -> bool:
        try:
            await OrderModel.create(**data.to_json)
            return True
        except Exception as error:
            logger.error(f"ERROR STEP 13: {error}")
            return False

    @staticmethod
    async def delete(api_name: str, user_id: int) -> bool:
        try:
            orders = await OrderModel.filter(api_name=api_name, user_id=user_id).all()
            if len(orders) > 0:
                for order in orders:
                    await OrderModel.delete(order)
            return True
        except Exception as error:
            logger.error(f"ERROR STEP 13: {error}")
            return False


class AccountController(DBShow, DBUpdate):
    @staticmethod
    async def show(api_name: str) -> Optional[MODEL]:
        return await AccountModel.get_or_none(api_name=api_name)

    @staticmethod
    async def update(data: UpdateAccountData) -> bool:
        try:
            account = await AccountModel.get(api_name=data.api_name)
            await account.update_from_dict(data=data.to_json)
            return True
        except Exception as error:
            logger.error(f"ERROR STEP 13: {error}")
            return False


class IncomeController(DBShow, DBCreate):
    pass
