from decimal import Decimal

import pytest

from apps.nbp.models import ExchangeRatePLN

pytestmark = pytest.mark.django_db


class TestExchangeRatePLN:
    def setup(self):
        self.exchange = ExchangeRatePLN.objects.create(
            date="2020-04-04", currency="USD", rate=Decimal(2.5213)
        )

    def test_str(self):
        assert str(self.exchange) == "2020-04-04 USD 2.5213"

    def test_exchange_to_pln(self):
        assert self.exchange.exchange_to_pln(Decimal(100)) == Decimal("252.13")

    def test_exchange_from_pln(self):
        assert self.exchange.exchange_from_pln(Decimal(250)) == Decimal("99.16")
