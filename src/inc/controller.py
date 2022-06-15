from typing import Optional

from src.models import OrderModel, AccountModel, IncomeModel
from src.inc.base_classes import DBShow, DBCreate, DBUpdate, DBDelete
from src.inc.schemas import CreateOrderData, CreateIncomeData
from src.inc.schemas import UpdateAccountData
from config import logger


class OrderController(DBCreate, DBDelete):
    """Order controller | Add new order & Delete ALL order"""
    @staticmethod
    async def create(data: CreateOrderData) -> bool:
        """Add new order"""
        try:
            await OrderModel.create(**data.to_json)
            return True
        except Exception as error:
            logger.error(f"ERROR STEP 13: {error}")
            return False

    @staticmethod
    async def delete(api_name: str, user_id: int) -> bool:
        """Delete ALL order"""
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
    """Account controller | Show account data & Update account information"""
    @staticmethod
    async def show(api_name: str) -> Optional[AccountModel]:
        """Show account data"""
        return await AccountModel.get_or_none(api_name=api_name)

    @staticmethod
    async def update(data: UpdateAccountData) -> bool:
        """Update account information"""
        try:
            account = await AccountModel.get(api_name=data.api_name)
            await account.update_from_dict(data=data.to_json)
            return True
        except Exception as error:
            logger.error(f"ERROR STEP 13: {error}")
            return False


class IncomeController(DBShow, DBCreate):
    """Income controller | Show latest income & Create new income"""
    @staticmethod
    async def show(api_name: str) -> Optional[IncomeModel]:
        """Show latest income data"""
        try:
            return await IncomeModel.filter().order_by(IncomeModel.time.desc()).limit(1).first()
        except Exception as error:
            logger.error(f"ERROR STEP 13: {error}")
            return None

    @staticmethod
    async def create(data: CreateIncomeData) -> bool:
        """Create new income"""
        try:
            await IncomeModel.create(**data.to_json)
            return True
        except Exception as error:
            logger.error(f"ERROR STEP 13: {error}")
            return False

