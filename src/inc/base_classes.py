from dataclasses import dataclass
from typing import Optional, Dict, Any

from tortoise.queryset import MODEL


# <<<==========================================>>> Database classes controller <<<===================================>>>


class DBRead:
    """Database class helper | Show data"""
    @staticmethod
    async def read(**kwargs: Any) -> Optional[MODEL]:
        raise NotImplementedError


class DBCreate:
    """Database class helper | Create new data"""
    @staticmethod
    async def create(data: dataclass) -> bool:
        raise NotImplementedError


class DBUpdate:
    """Database class helper | Update data"""
    @staticmethod
    async def update(data: dataclass) -> bool:
        raise NotImplementedError


class DBDelete:
    """Database class helper | Delete data"""
    @staticmethod
    async def delete(**kwargs: Any) -> bool:
        raise NotImplementedError


class CRUD(DBCreate, DBRead, DBUpdate, DBDelete):
    pass


# <<<==========================================>>> JSON helper <<<===================================================>>>


class ToJson:
    @property
    def to_json(self) -> Dict:
        raise NotImplementedError


class FullJSON:
    @property
    def full_json(self):
        raise NotImplementedError
