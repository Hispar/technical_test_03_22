import csv
import logging
import os
from datetime import datetime
from decimal import Decimal

from django.utils.timezone import make_aware

from example.models import Coin, CoinMarketData

logger = logging.getLogger(__name__)


class CsvEtl:
    OPERATION_ID = 0
    NAME = 1
    SYMBOL = 2
    DATE = 3
    HIGH = 4
    LOW = 5
    OPEN = 6
    CLOSE = 7
    VOLUME = 8
    MARKETCAP = 9

    @classmethod
    def load_from_directory(cls, directory: str):
        for filename in os.listdir(directory):
            file = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(file):
                logger.info(file)
                cls.load_file(file)

    @classmethod
    def load_file(cls, file):
        with open(file) as csvfile:
            datareader = csv.reader(csvfile)
            header = next(datareader)
            if header:
                for row in datareader:
                    cls.load_row(row)

    @classmethod
    def load_row(cls, row):
        coin, created = Coin.objects.get_or_create(
            name=row[cls.NAME], symbol=row[cls.SYMBOL]
        )
        try:
            CoinMarketData.objects.get_or_create(
                coin=coin,
                operation_id=row[cls.OPERATION_ID],
                defaults={
                    "date": cls.get_date(row, cls.DATE),
                    "high": cls.get_decimal(row, cls.HIGH),
                    "low": cls.get_decimal(row, cls.LOW),
                    "open": cls.get_decimal(row, cls.OPEN),
                    "close": cls.get_decimal(row, cls.CLOSE),
                    "volume": cls.get_decimal(row, cls.VOLUME),
                    "marketcap": cls.get_decimal(row, cls.MARKETCAP),
                },
            )
        except Exception as e:
            logger.exception(e, extra={"row": row})

    @classmethod
    def get_decimal(cls, row, index):
        try:
            return Decimal(row[index])
        except Exception as e:
            logger.exception(e, extra={"row": row, "index": index})
            return Decimal(0)

    @classmethod
    def get_date(cls, row, index):
        return make_aware(datetime.strptime(row[index], "%Y-%m-%d %H:%M:%S"))
