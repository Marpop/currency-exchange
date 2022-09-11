from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

from apps.nbp.choices import Currency

pytestmark = pytest.mark.django_db


class TestExchangeRateView:
    def setup(self):
        self.url = "{}?date={}&currency_input={}&currency_output={}&amount={}"
        self.url_test_statuses = self.url.format(
            reverse("api:nbp:exchange"),
            "2020-04-04",
            str(Currency.USD),
            str(Currency.PLN),
            100,
        )
        self.api_client = APIClient()
        self.mocker_path = "apps.nbp.services.NBP_API.exchange"

    def test_get_200(self, mocker):
        get_exchange_rate = mocker.patch(
            self.mocker_path,
            return_value=Response({str(Currency.PLN): 250}, status=status.HTTP_200_OK),
        )
        response = self.api_client.get(self.url_test_statuses)
        get_exchange_rate.assert_called_once()
        assert response.json() == {str(Currency.PLN): 250}
        assert response.status_code == status.HTTP_200_OK
        assert get_exchange_rate.call_count == 1

    def test_get_404(self, mocker):
        get_exchange_rate = mocker.patch(
            self.mocker_path,
            return_value=Response(status=status.HTTP_404_NOT_FOUND),
        )
        response = self.api_client.get(self.url_test_statuses)
        get_exchange_rate.assert_called_once()
        assert response.json() == {"detail": "Not found."}
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert get_exchange_rate.call_count == 1

    def test_get_400(self, mocker):
        get_exchange_rate = mocker.patch(
            self.mocker_path,
            return_value=Response(status=status.HTTP_400_BAD_REQUEST),
        )
        response = self.api_client.get(self.url_test_statuses)
        get_exchange_rate.assert_called_once()
        assert response.json() == {"detail": "Not found."}
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert get_exchange_rate.call_count == 1

    def test_get_503(self, mocker):
        get_exchange_rate = mocker.patch(
            self.mocker_path,
            return_value=Response(status=status.HTTP_503_SERVICE_UNAVAILABLE),
        )
        response = self.api_client.get(self.url_test_statuses)
        get_exchange_rate.assert_called_once()
        assert response.json() == {"detail": "Service unavailable."}
        assert response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE
        assert get_exchange_rate.call_count == 1

    @pytest.mark.parametrize(
        "date, currency_input, currency_output, amount, response_data",
        [
            (
                "2020-04-",
                str(Currency.USD),
                str(Currency.PLN),
                100,
                {
                    "date": [
                        "Date has wrong format. Use one of these formats instead: YYYY-MM-DD."
                    ]
                },
            ),
            (
                "2020-04-04",
                str(Currency.USD),
                str(Currency.USD),
                100,
                {"non_field_errors": ["Currency input and output cannot be the same."]},
            ),
            (
                "2020-04-04",
                "AAA",
                str(Currency.USD),
                100,
                {"currency_input": ['"AAA" is not a valid choice.']},
            ),
            (
                "2020-04-04",
                str(Currency.USD),
                "AAA",
                100,
                {"currency_output": ['"AAA" is not a valid choice.']},
            ),
            (
                "2020-04-04",
                "USD",
                str(Currency.PLN),
                "AAA",
                {"amount": ["A valid number is required."]},
            ),
        ],
    )
    def test_get_validation(  # pylint: disable=too-many-arguments
        self,
        date,
        currency_input,
        currency_output,
        amount,
        response_data,
    ):
        url = self.url.format(
            reverse("api:nbp:exchange"), date, currency_input, currency_output, amount
        )
        response = self.api_client.get(url)
        assert response.json() == response_data
        assert response.status_code == status.HTTP_400_BAD_REQUEST
