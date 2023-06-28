# -*- coding: utf-8 -*-
# Python imports
# 3rd Party imports
import unittest
from decimal import Decimal

from django.test import testcases

# App imports
from example.etl import CsvEtl
from example.models import Coin, CoinMarketData


class CsvEtlTestCase(testcases.TestCase):
    def example_row(self):
        return "1,Aave,AAVE,2020-10-05 23:59:59,55.11235847,49.78789992,52.67503496,53.21924296,0.0,89128128.86084658".split(
            ","
        )

    def test_load_row(self):
        row = self.example_row()
        assert Coin.objects.all().count() == 0
        assert CoinMarketData.objects.all().count() == 0
        CsvEtl.load_row(row)
        assert Coin.objects.all().count() == 1
        assert CoinMarketData.objects.all().count() == 1

        coin = Coin.objects.last()
        assert coin.name == row[1]
        assert coin.symbol == row[2]

        coin_data = CoinMarketData.objects.last()
        assert coin_data.low == Decimal(row[5])
        assert coin_data.open == Decimal(row[6])
        assert coin_data.close == Decimal(row[7])


if __name__ == "__main__":
    unittest.main()
