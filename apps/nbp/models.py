from django.db import models


class ExchangeRate(models.Model):
    class Currency(models.TextChoices):
        PLN = "PLN", "Polish Zloty"
        USD = "USD", "US Dollar"
        EUR = "EUR", "Euro"
        CHF = "CHF", "CHF"
        GBP = "JPY", "Japanese Yen"

    date = models.DateField(
        "date",
    )
    amount = models.DecimalField("amount", max_digits=60, decimal_places=2)
    currency_input = models.CharField(
        "currency input", choices=Currency.choices, max_length=3
    )
    currency_output = models.CharField(
        "currency output", choices=Currency.choices, max_length=3
    )
