from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.test import APIClient

from apps.nbp.choices import Currency

pytestmark = pytest.mark.django_db


class TestExchangeRateView:
    def setup(self):
        self.url = "{}?date={}&currency_input={}&currency_output={}&amount={}"
        self.api_client = APIClient()

    def test_get_ok(self, mocker):
        get_exchange_rate = mocker.patch(
            "apps.nbp.services.NBP_API.exchange",
            return_value=250,
        )
        response = self.api_client.get(
            self.url.format(
                reverse("api:nbp:exchange"),
                "2020-04-07",
                Currency.USD.name,
                Currency.PLN.name,
                100,
            )
        )
        assert response.json() == {Currency.PLN.name: 250}
        assert response.status_code == status.HTTP_200_OK
        assert get_exchange_rate.call_count == 1

    @pytest.mark.parametrize(
        "date, currency_input, currency_output, amount, response_data",
        [
            (
                "2020-04-",
                Currency.USD.name,
                Currency.PLN.name,
                100,
                {
                    "date": [
                        "Date has wrong format. Use one of these formats instead: YYYY-MM-DD."
                    ]
                },
            ),
            (
                "2020-04-07",
                Currency.USD.name,
                Currency.USD.name,
                100,
                {"non_field_errors": ["Currency input and output cannot be the same."]},
            ),
            (
                "2020-04-07",
                "AAA",
                Currency.USD.name,
                100,
                {"currency_input": ['"AAA" is not a valid choice.']},
            ),
            (
                "2020-04-07",
                Currency.USD.name,
                "AAA",
                100,
                {"currency_output": ['"AAA" is not a valid choice.']},
            ),
            (
                "2020-04-07",
                "USD",
                Currency.PLN.name,
                "AAA",
                {"amount": ["A valid number is required."]},
            ),
            (
                "2001-04-07",
                Currency.USD.name,
                Currency.PLN.name,
                100,
                {"date": ["Date cannot be before 2002-01-02."]},
            ),
            (
                "9999-04-07",
                Currency.USD.name,
                Currency.PLN.name,
                100,
                {"date": ["Date cannot be in the future."]},
            ),
            (
                "2020-04-04",
                Currency.USD.name,
                Currency.PLN.name,
                100,
                {"date": ["Date cannot be a weekend day."]},
            ),
        ],
    )
    def test_get_bad_request(  # pylint: disable=too-many-arguments
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
