import datetime
import logging
from decimal import Decimal

import requests
from rest_framework import status

from apps.nbp.choices import Currency
from apps.nbp.exceptions import ServiceNotFound, ServiceUnavailable
from apps.nbp.models import ExchangeRatePLN


class NBP_API:
    def __init__(self) -> None:
        self.rates_a_url = "http://api.nbp.pl/api/exchangerates/rates/a"
        self.logger = logging.getLogger("NBP API")
        self.timeout = 3

    def _fetch_exchange_response(self, code: str, date: datetime.date) -> dict:
        try:
            response = requests.get(
                url=f"{self.rates_a_url}/{code}/{str(date)}/",
                timeout=self.timeout,
                headers={"Content-Type": "application/json"},
            )
            if response.status_code != status.HTTP_200_OK:
                self.logger.error(f"{date} {code} {response}")
                raise ServiceNotFound
            self.logger.info(f"{date} {code} exchange get")
            return response.json()
        except requests.exceptions.RequestException as error:
            self.logger.error(f"Request error: {error}")
            raise ServiceUnavailable from error

    def _fetch_exchange_rate(self, code: str, date: datetime.date) -> str:
        response = self._fetch_exchange_response(code, date)
        return response["rates"][0]["mid"]

    def _get_exchange_rate_pln(self, code: str, date: datetime.date) -> ExchangeRatePLN:
        try:
            exchange_rate_pln = ExchangeRatePLN.objects.get(date=date, currency=code)
        except ExchangeRatePLN.DoesNotExist:
            exchange_rate = self._fetch_exchange_rate(code, date)
            exchange_rate_pln = ExchangeRatePLN.objects.create(
                date=date,
                currency=code,
                rate=exchange_rate,
            )
        return exchange_rate_pln

    def exchange(
        self,
        date: datetime.date,
        currency_input: str,
        currency_output: str,
        amount: Decimal,
    ) -> Decimal:

        if currency_input == Currency.PLN:
            exchange_rate_pln = self._get_exchange_rate_pln(currency_output, date)
            return exchange_rate_pln.exchange_from_pln(amount)
        if currency_output == Currency.PLN:
            exchange_rate_pln = self._get_exchange_rate_pln(currency_input, date)
            return exchange_rate_pln.exchange_to_pln(amount)

        # both currencies are not PLN
        exchange_rate_pln_input = self._get_exchange_rate_pln(currency_input, date)
        exchange_rate_pln_output = self._get_exchange_rate_pln(currency_output, date)

        return exchange_rate_pln_output.exchange_from_pln(
            exchange_rate_pln_input.exchange_to_pln(amount)
        )
