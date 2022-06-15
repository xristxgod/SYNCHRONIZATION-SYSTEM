import os
import logging
import decimal

decimals = decimal.Context()
decimals.prec = 8

logger = logging.getLogger(__name__)


class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    BINANCE_API_URL = ""
