from django.db import models

from apps.nbp.choices import CurrencyExchangePLN


class ExchangeRatePLN(models.Model):

    date = models.DateField(
        "date",
    )
    currency = models.CharField(
        "currency", choices=CurrencyExchangePLN.choices, max_length=3
    )
    rate = models.DecimalField(max_digits=10, decimal_places=4)
