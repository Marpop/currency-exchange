import datetime

from rest_framework import status

from apps.nbp.choices import CurrencyExchangePLN
from apps.nbp.services import NBP_API


class Test_NBP_API:
    def setup(self):
        self.nbp_api = NBP_API()
        self.code = str(CurrencyExchangePLN.USD)
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

    def test__get_exchange_response_200(self, requests_mock):
        requests_mock.get(
            url=self.url, json=self.response_ok, status_code=status.HTTP_200_OK
        )
        response = self.nbp_api._get_exchange_response(self.code, self.date)
        assert response.data == self.response_ok
        assert response.status_code == status.HTTP_200_OK
        assert requests_mock.call_count == 1

    def test__get_exchange_response_404(self, requests_mock):
        requests_mock.get(url=self.url, status_code=status.HTTP_404_NOT_FOUND)
        response = self.nbp_api._get_exchange_response(self.code, self.date)
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert requests_mock.call_count == 1

    def test__get_exchange_response_400(self, requests_mock):
        requests_mock.get(url=self.url, status_code=status.HTTP_400_BAD_REQUEST)
        response = self.nbp_api._get_exchange_response(self.code, self.date)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert requests_mock.call_count == 1
