import os
import logging
import decimal

decimals = decimal.Context()
decimals.prec = 8


class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
