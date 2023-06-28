from ninja import ModelSchema
from pydantic import Field

from example.models import Coin, CoinMarketData


class CoinSchema(ModelSchema):
    class Config:
        model = Coin
        model_fields = ["name", "symbol"]


class CoinMarketDataSchema(ModelSchema):
    coin: str = Field(..., alias="coin.name")

    class Config:
        model = CoinMarketData
        model_fields = [
            "id",
            "operation_id",
            "date",
            "high",
            "low",
            "open",
            "close",
            "volume",
            "marketcap",
        ]


class CoinMarketDataListSchema(ModelSchema):
    class Config:
        model = CoinMarketData
        model_fields = ["date", "high", "low", "open", "close", "volume", "marketcap"]
