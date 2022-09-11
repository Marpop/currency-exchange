import datetime
import logging
from decimal import Decimal

import requests
from rest_framework import status
from rest_framework.response import Response

from apps.nbp.choices import Currency
from apps.nbp.models import ExchangeRatePLN


class NBP_API:
    def __init__(self) -> None:
        self.rates_a_url = "http://api.nbp.pl/api/exchangerates/rates/a"
        self.logger = logging.getLogger("NBP API")
        self.timeout = 3

    def _fetch_exchange_response(self, code: str, date: datetime.date) -> Response:
        try:
            response = requests.get(
                url=f"{self.rates_a_url}/{code}/{str(date)}/",
                timeout=self.timeout,
                headers={"Content-Type": "application/json"},
            )
            if response.status_code == status.HTTP_200_OK:
                self.logger.info(f"{date} {code} exchange get")
                return Response(response.json(), status=status.HTTP_200_OK)
            self.logger.error(f"{date} {code} {response}")
            return Response(status=response.status_code)
        except requests.exceptions.RequestException as error:
            self.logger.error(f"Request error: {error}")
            return Response(status=status.HTTP_503_SERVICE_UNAVAILABLE)

    def _fetch_exchange_rate(self, code: str, date: datetime.date) -> Response:
        response = self._fetch_exchange_response(code, date)
        if response.status_code == status.HTTP_200_OK:
            return Response(
                {"rate": response.data["rates"][0]["mid"]},
                status=status.HTTP_200_OK,
            )
        return Response(status=response.status_code)

    def _exchange_pln(self, date, currency_input, currency_output, amount):
        if currency_input == Currency.PLN:
            rated_currency = currency_output
        if currency_output == Currency.PLN:
            rated_currency = currency_input

        try:
            exchange_rate = ExchangeRatePLN.objects.get(
                date=date, currency=rated_currency
            )
        except ExchangeRatePLN.DoesNotExist:
            nbp_response = self._fetch_exchange_rate(rated_currency, date)
            if nbp_response.status_code == status.HTTP_200_OK:
                exchange_rate = ExchangeRatePLN.objects.create(
                    date=date,
                    currency=rated_currency,
                    rate=Decimal(nbp_response.data["rate"]),
                )
            else:
                return nbp_response

        if currency_input == Currency.PLN:
            result = exchange_rate.exchange_to_pln(amount)
        if currency_output == Currency.PLN:
            result = exchange_rate.exchange_from_pln(amount)

        return Response(
            {rated_currency: result},
            status=status.HTTP_200_OK,
        )

    def _exchange_not_pln(self, date, currency_input, currency_output, amount):
        try:
            exchange_rate_input = ExchangeRatePLN.objects.get(
                date=date, currency=currency_input
            )
        except ExchangeRatePLN.DoesNotExist:
            nbp_response = self._fetch_exchange_rate(currency_input, date)
            if nbp_response.status_code == status.HTTP_200_OK:
                exchange_rate_input = ExchangeRatePLN.objects.create(
                    date=date,
                    currency=currency_input,
                    rate=Decimal(nbp_response.data["rate"]),
                )
            else:
                return nbp_response
        try:
            exchange_rate_output = ExchangeRatePLN.objects.get(
                date=date, currency=currency_output
            )
        except ExchangeRatePLN.DoesNotExist:
            nbp_response = self._fetch_exchange_rate(currency_output, date)
            if nbp_response.status_code == status.HTTP_200_OK:
                exchange_rate_output = ExchangeRatePLN.objects.create(
                    date=date,
                    currency=currency_output,
                    rate=Decimal(nbp_response.data["rate"]),
                )
            else:
                return nbp_response
        return Response(
            {
                currency_input: exchange_rate_output.exchange_from_pln(
                    exchange_rate_input.exchange_to_pln(amount)
                )
            },
            status=status.HTTP_200_OK,
        )

    def exchange(self, date, currency_input, currency_output, amount):
        # one of currencies is PLN
        if Currency.PLN in (currency_input, currency_output):
            return self._exchange_pln(date, currency_input, currency_output, amount)

        # both currencies are not PLN
        return self._exchange_not_pln(date, currency_input, currency_output, amount)
