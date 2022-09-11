import datetime
from decimal import Decimal

import pytest
import requests
from rest_framework import status

from apps.nbp.choices import Currency, CurrencyExchangePLN
from apps.nbp.exceptions import ServiceNotFound, ServiceUnavailable
from apps.nbp.models import ExchangeRatePLN
from apps.nbp.services import NBP_API

pytestmark = pytest.mark.django_db


class Test_NBP_API:
    def setup(self):
        self.nbp_api = NBP_API()
        self.code = CurrencyExchangePLN.USD.name
        self.date = datetime.date(2016, 4, 4)
        self.url = f"{self.nbp_api.rates_a_url}/{self.code}/{str(self.date)}/"
        self.response_ok = {
            "table": "A",
            "currency": "dolar amerykański",
            "code": "USD",
            "rates": [
                {
                    "no": "064/A/NBP/2016",
                    "effectiveDate": "2016-04-04",
                    "mid": 3.7254,
                }
            ],
        }

    def test__fetch_exchange_response_200(self, requests_mock):
        requests_mock.get(
            url=self.url, json=self.response_ok, status_code=status.HTTP_200_OK
        )
        response = self.nbp_api._fetch_exchange_response(self.code, self.date)
        assert response == self.response_ok
        assert requests_mock.call_count == 1

    def test__fetch_exchange_response_404(self, requests_mock):
        requests_mock.get(url=self.url, status_code=status.HTTP_404_NOT_FOUND)
        with pytest.raises(ServiceNotFound):
            self.nbp_api._fetch_exchange_response(self.code, self.date)
            assert requests_mock.call_count == 1

    def test__fetch_exchange_response_400(self, requests_mock):
        requests_mock.get(url=self.url, status_code=status.HTTP_400_BAD_REQUEST)
        with pytest.raises(ServiceNotFound):
            self.nbp_api._fetch_exchange_response(self.code, self.date)
            assert requests_mock.call_count == 1

    def test__fetch_exchange_response_503(self, requests_mock):
        requests_mock.get(url=self.url, exc=requests.exceptions.ConnectTimeout)
        with pytest.raises(ServiceUnavailable):
            self.nbp_api._fetch_exchange_response(self.code, self.date)
            assert requests_mock.call_count == 1

    def test__fetch_exchange_rate(self, mocker):
        _fetch_exchange_response = mocker.patch(
            "apps.nbp.services.NBP_API._fetch_exchange_response",
            return_value=self.response_ok,
        )
        response = self.nbp_api._fetch_exchange_rate(self.code, self.date)
        assert response == 3.7254
        assert _fetch_exchange_response.call_count == 1

    @pytest.mark.parametrize(
        "currency_input, currency_output, expected_response",
        [
            (Currency.PLN.name, Currency.USD.name, 40),
            (Currency.USD.name, Currency.PLN.name, 250),
            (Currency.USD.name, Currency.GBP.name, Decimal("47.28")),
        ],
    )
    def test_exchange(self, currency_input, currency_output, expected_response):
        ExchangeRatePLN.objects.create(
            date=self.date,
            currency=Currency.USD,
            rate=2.5,
        )
        ExchangeRatePLN.objects.create(
            date=self.date,
            currency=Currency.GBP,
            rate=3,
        )
        response = self.nbp_api.exchange(
            self.date,
            currency_input=currency_input,
            currency_output=currency_output,
            amount=Decimal("100"),
        )
        assert response == expected_response
