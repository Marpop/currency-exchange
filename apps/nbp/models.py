from decimal import Decimal

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

    class Meta:
        unique_together = ("date", "currency")

    def __str__(self):
        return f"{self.date} {self.currency} {round(self.rate, 4)}"

    def exchange_to_pln(self, amount: Decimal) -> Decimal:
        return round(amount * Decimal(self.rate), 2)

    def exchange_from_pln(self, amount: Decimal) -> Decimal:
        return round(amount / Decimal(self.rate), 2)
