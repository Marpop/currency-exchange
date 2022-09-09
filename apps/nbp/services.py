import datetime
import logging

import requests
from rest_framework import status
from rest_framework.response import Response


class NBP_API:
    def __init__(self) -> None:
        self.rates_a_url = "http://api.nbp.pl/api/exchangerates/rates/a"
        self.logger = logging.getLogger("NBP API")
        self.timeout = 3

    def get_exchange_response(self, code: str, date: datetime.date) -> Response:
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
