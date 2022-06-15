from typing import Optional

from src.models import OrderModel, AccountModel, IncomeModel, PositionModel
from src.inc.base_classes import DBRead, DBCreate, DBUpdate, DBDelete, CRUD
from src.inc.schemas import CreateOrderData, CreateIncomeData, CUPositionData
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
            logger.error(f"ERROR STEP 16: {error}")
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
            logger.error(f"ERROR STEP 26: {error}")
            return False


class AccountController(DBRead, DBUpdate):
    """Account controller | Show account data & Update account information"""
    @staticmethod
    async def read(api_name: str) -> Optional[AccountModel]:
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
            logger.error(f"ERROR STEP 47: {error}")
            return False


class IncomeController(DBCreate, DBRead):
    """Income controller | Show latest income & Create new income"""
    @staticmethod
    async def create(data: CreateIncomeData) -> bool:
        """Create new income"""
        try:
            await IncomeModel.create(**data.to_json)
            return True
        except Exception as error:
            logger.error(f"ERROR STEP 61: {error}")
            return False

    @staticmethod
    async def read(api_name: str, user_id: int) -> Optional[IncomeModel]:
        """Show latest income data"""
        try:
            return await IncomeModel.filter(
                api_name=api_name, user_id=user_id
            ).order_by(IncomeModel.time.desc()).limit(1).first()
        except Exception as error:
            logger.error(f"ERROR STEP 71: {error}")
            return None


class PositionController(CRUD):
    """Position controller | CRUD"""
    @staticmethod
    async def create(data: CUPositionData) -> bool:
        """Create new position"""
        try:
            await PositionModel.create(**data.full_json)
            return True
        except Exception as error:
            logger.error(f"ERROR STEP 85: {error}")
            return False

    @staticmethod
    async def read(api_name: str, user_id: int) -> Optional[PositionModel]:
        """Show position"""
        return await PositionModel.get_or_none(api_name=api_name, user_id=user_id)

    @staticmethod
    async def update(data: CUPositionData) -> bool:
        """Update position"""
        try:
            position = await PositionModel.get(api_name=data.api_name, user_id=data.user_id)
            await position.update_from_dict(data=data.to_json)
            return True
        except Exception as error:
            logger.error(f"ERROR STEP 100: {error}")
            return False

    @staticmethod
    async def delete(api_name: str, user_id: int) -> bool:
        """Delete ALL position"""
        try:
            positions = await PositionModel.filter(api_name=api_name, user_id=user_id).all()
            if len(positions) > 0:
                for position in positions:
                    await PositionModel.delete(position)
            return True
        except Exception as error:
            logger.error(f"ERROR STEP 111: {error}")
            return False
