from django.db import models


class CurrencyExchangePLN(models.TextChoices):
    USD = "USD", "US Dollar"
    EUR = "EUR", "Euro"
    CHF = "CHF", "Swiss Franc"
    GBP = "JPY", "Japanese Yen"


class Currency(models.TextChoices):
    PLN = "PLN", "Polish Zloty"
    USD = "USD", "US Dollar"
    EUR = "EUR", "Euro"
    CHF = "CHF", "Swiss Franc"
    GBP = "JPY", "Japanese Yen"
