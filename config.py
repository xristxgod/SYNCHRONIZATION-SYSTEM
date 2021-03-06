import os
import logging
import decimal

decimals = decimal.Context()
decimals.prec = 8

logger = logging.getLogger(__name__)


class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite://db.sqlite3")
    BINANCE_API_URL = ""
    SLEEP_TIME = 1500
    VERSION = "0.01"
