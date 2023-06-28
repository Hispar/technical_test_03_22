from django.db import models
from django.db.models import CASCADE
from django.utils.translation import gettext_lazy as _
from model_utils.models import TimeStampedModel


class Coin(TimeStampedModel):
    name = models.CharField(max_length=255, null=False, blank=False)
    symbol = models.CharField(max_length=255, null=False, blank=False)

    def __str__(self):
        return "{}: {} - {}".format(self.__class__.__name__, self.pk, self.name)

    class Meta:
        verbose_name = _("Coin")
        verbose_name_plural = _("Coins")


class CoinMarketData(TimeStampedModel):
    coin = models.ForeignKey(Coin, related_name="market_data", on_delete=CASCADE)
    operation_id = models.IntegerField(null=False, blank=False)
    date = models.DateTimeField(default=0)
    high = models.DecimalField(default=0, decimal_places=20, max_digits=40)
    low = models.DecimalField(default=0, decimal_places=20, max_digits=40)
    open = models.DecimalField(default=0, decimal_places=20, max_digits=40)
    close = models.DecimalField(default=0, decimal_places=20, max_digits=40)
    volume = models.DecimalField(default=0, decimal_places=20, max_digits=40)
    marketcap = models.DecimalField(default=0, decimal_places=20, max_digits=40)

    def __str__(self):
        return "{}: {} - {} - {}".format(
            self.__class__.__name__, self.pk, self.coin, self.date
        )

    class Meta:
        verbose_name = _("CoinMarketData")
        verbose_name_plural = _("CoinMarketData")
