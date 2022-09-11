import datetime

import pytest
import requests
from rest_framework import status
from rest_framework.response import Response

from apps.nbp.choices import Currency, CurrencyExchangePLN
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
        assert response.data == self.response_ok
        assert response.status_code == status.HTTP_200_OK
        assert requests_mock.call_count == 1

    def test__fetch_exchange_response_404(self, requests_mock):
        requests_mock.get(url=self.url, status_code=status.HTTP_404_NOT_FOUND)
        response = self.nbp_api._fetch_exchange_response(self.code, self.date)
        assert not response.data
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert requests_mock.call_count == 1

    def test__fetch_exchange_response_400(self, requests_mock):
        requests_mock.get(url=self.url, status_code=status.HTTP_400_BAD_REQUEST)
        response = self.nbp_api._fetch_exchange_response(self.code, self.date)
        assert not response.data
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert requests_mock.call_count == 1

    def test__fetch_exchange_response_503(self, requests_mock):
        requests_mock.get(url=self.url, exc=requests.exceptions.ConnectTimeout)
        response = self.nbp_api._fetch_exchange_response(self.code, self.date)
        assert not response.data
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert requests_mock.call_count == 1

    @pytest.mark.parametrize(
        "expected_response, status_code",
        [({"rate": 3.7254}, status.HTTP_200_OK), (None, status.HTTP_404_NOT_FOUND)],
    )
    def test__fetch_exchange_rate(self, expected_response, status_code, mocker):
        _fetch_exchange_response = mocker.patch(
            "apps.nbp.services.NBP_API._fetch_exchange_response",
            return_value=Response(self.response_ok, status=status_code),
        )
        response = self.nbp_api._fetch_exchange_rate(self.code, self.date)
        assert response.data == expected_response
        assert response.status_code == status_code
        assert _fetch_exchange_response.call_count == 1

    @pytest.mark.parametrize(
        "currency_input, currency_output, mocker_path",
        [
            (
                Currency.PLN.name,
                Currency.USD.name,
                "apps.nbp.services.NBP_API._exchange_pln",
            ),
            (
                Currency.USD.name,
                Currency.PLN.name,
                "apps.nbp.services.NBP_API._exchange_pln",
            ),
            (
                Currency.USD.name,
                Currency.GBP.name,
                "apps.nbp.services.NBP_API._exchange_not_pln",
            ),
        ],
    )
    def test_exchange(self, currency_input, currency_output, mocker_path, mocker):
        mocker = mocker.patch(
            mocker_path,
            return_value=Response({currency_output: 26.81}, status=status.HTTP_200_OK),
        )
        response = self.nbp_api.exchange(
            self.date,
            currency_input=currency_input,
            currency_output=currency_output,
            amount=100,
        )
        assert response.data == {currency_output: 26.81}
        assert response.status_code == status.HTTP_200_OK
        assert mocker.call_count == 1
