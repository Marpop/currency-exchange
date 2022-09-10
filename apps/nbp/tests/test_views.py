from django.urls import reverse

import pytest
from rest_framework import status
from rest_framework.response import Response
from rest_framework.test import APIClient

pytestmark = pytest.mark.django_db


class TestExchangeRateView:
    def setup(self):
        self.url = "api:nbp:exchange"
        self.api_client = APIClient()
        self.mocker_path = "apps.nbp.services.NBP_API.exchange"

    def test_get_exchange_rate_200(self, mocker):
        get_exchange_rate = mocker.patch(
            self.mocker_path,
            return_value=Response({"rate": 3.7254}, status=status.HTTP_200_OK),
        )
        url = reverse(
            self.url,
            kwargs={
                "date": "2016-04-04",
                "currency_input": "USD",
                "currency_output": "PLN",
                "amount": 2,
            },
        )
        response = self.api_client.get(url)
        assert response.data == {"PLN": 7.45}
        assert response.status_code == status.HTTP_200_OK
        get_exchange_rate.assert_called_once()
