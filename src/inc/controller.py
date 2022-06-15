from urllib.parse import urlencode
from typing import Optional, Tuple

from src.models import OrderModel, AccountModel, IncomeModel, PositionModel
from src.types import API_NAME
from src.inc.base_classes import DBRead, DBCreate, DBUpdate, DBDelete, CRUD
from src.inc.schemas import CreateOrderData, CreateIncomeData, CUPositionData, UpdateAccountData
from src.inc.schemas import RequestPublicData, RequestPrivateData
from src.external.client import client
from src.utils.exceptions import HTTPRequestError
from src.utils.utils import utils
from config import Config, logger


# <<<==========================================>>> Database Controller <<<===========================================>>>


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
    async def delete(api_name: API_NAME, user_id: int) -> bool:
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
    async def read(api_name: API_NAME, user_id: int) -> Optional[IncomeModel]:
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
    async def read(api_name: API_NAME, user_id: int, **kwargs) -> Optional[PositionModel]:
        """Show position"""
        return await PositionModel.get_or_none(
            api_name=api_name, user_id=user_id, symbol=kwargs.get("symbol"), positionSide=kwargs.get("positionSide")
        )

    @staticmethod
    async def update(data: CUPositionData) -> bool:
        """Update position"""
        try:
            position = await PositionModel.get(api_name=data.api_name, user_id=data.user_id)
            await position.update_from_dict(data=data.to_json)
            return True
        except Exception as error:
            logger.error(f"ERROR STEP 110: {error}")
            return False

    @staticmethod
    async def delete(api_name: API_NAME, user_id: int) -> bool:
        """Delete ALL position"""
        try:
            positions = await PositionModel.filter(api_name=api_name, user_id=user_id).all()
            if len(positions) > 0:
                for position in positions:
                    await PositionModel.delete(position)
            return True
        except Exception as error:
            logger.error(f"ERROR STEP 121: {error}")
            return False


# <<<==========================================>>> Request Controller <<<===========================================>>>


class RequestController:
    """Request Controller | Private method & Public method"""
    @staticmethod
    async def private(data: RequestPrivateData) -> Optional[Tuple]:
        """Private method"""
        response_session = None
        try:
            query = urlencode(data.payload).replace("%27", "%22")
            query = f"{query}&timestamp={utils.get_timestamp_now()}" if query else f"timestamp={utils.get_timestamp_now()}"
            url = utils.convert_to_url(
                Config.BINANCE_API_URL, data.urlPath, "?", query, "&signature=", utils.hashing(query, data.apiData[1])
            )
            params = {"url": url, "params": {}}
            response_session = (await client.dispatch(api_key=data.apiData[0], method=data.httpMethod))(**params)
            response_data = await response_session.json()
            if "code" in response_data:
                raise HTTPRequestError(url=url, code=response_data["code"], msg=response_data["msg"])
            return response_session.headers, response_data
        except Exception as error:
            logger.error(f"ERROR STEP 141: {error}")
            return None
        finally:
            if response_session is not None:
                await response_session.close()

    @staticmethod
    async def public(data: RequestPublicData) -> Optional[Tuple]:
        """Public method"""
        response_session = None
        try:
            query = urlencode(data.payload, True)
            if query:
                url = utils.convert_to_url(Config.BINANCE_API_URL, data.urlPath, f"?{query}")
            else:
                url = utils.convert_to_url(Config.BINANCE_API_URL, data.urlPath)
            response_session = (await client.dispatch(method="GET"))(url=url)
            response_data = await response_session.json()
            if "code" in response_data:
                raise HTTPRequestError(url=url, code=response_data["code"], msg=response_data["msg"])
            return response_session.headers, response_data
        except Exception as error:
            logger.error(f"ERROR STEP 164: {error}")
            return None
        finally:
            if response_session is not None:
                await response_session.close()


# <<<==========================================>>> Runer <<<=========================================================>>>


account_controller = AccountController
order_controller = OrderController
income_controller = IncomeController
position_controller = PositionController
request_controller = RequestController
