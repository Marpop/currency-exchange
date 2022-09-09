# from decimal import Decimal

from decimal import Decimal

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.nbp.choices import Currency
from apps.nbp.models import ExchangeRatePLN
from apps.nbp.serializers import ExchangeRateSerializer
from apps.nbp.services import NBP_API


class ExchangeRateView(APIView):
    @extend_schema(parameters=[ExchangeRateSerializer])
    def get(self, request):
        serializer = ExchangeRateSerializer(
            data=request.query_params,
        )
        if serializer.is_valid():
            date = serializer.validated_data["date"]
            currency_input = serializer.validated_data["currency_input"]
            currency_output = serializer.validated_data["currency_output"]
            amount = serializer.validated_data["amount"]

            if currency_input == Currency.PLN:
                try:
                    exchange_rate = ExchangeRatePLN.objects.get(
                        date=date, currency=currency_output
                    )
                except ExchangeRatePLN.DoesNotExist:
                    nbp_response = NBP_API().get_exchange_response(
                        currency_output, date
                    )
                    if nbp_response.status_code == status.HTTP_200_OK:
                        exchange_rate = ExchangeRatePLN.objects.create(
                            date=date,
                            currency=currency_output,
                            rate=Decimal(nbp_response.data["rates"][0]["mid"]),
                        )
                    else:
                        return nbp_response
                return Response(
                    {currency_output: exchange_rate.exchange_from_pln(amount)},
                    status=status.HTTP_200_OK,
                )
            elif currency_output == Currency.PLN:
                try:
                    exchange_rate = ExchangeRatePLN.objects.get(
                        date=date, currency=currency_input
                    )
                except ExchangeRatePLN.DoesNotExist:
                    nbp_response = NBP_API().get_exchange_response(currency_input, date)
                    if nbp_response.status_code == status.HTTP_200_OK:
                        exchange_rate = ExchangeRatePLN.objects.create(
                            date=date,
                            currency=currency_input,
                            rate=Decimal(nbp_response.data["rates"][0]["mid"]),
                        )
                    else:
                        return nbp_response
                return Response(
                    {currency_input: exchange_rate.exchange_to_pln(amount)},
                    status=status.HTTP_200_OK,
                )
            else:
                try:
                    exchange_rate_input = ExchangeRatePLN.objects.get(
                        date=date, currency=currency_input
                    )
                except ExchangeRatePLN.DoesNotExist:
                    nbp_response = NBP_API().get_exchange_response(currency_input, date)
                    if nbp_response.status_code == status.HTTP_200_OK:
                        exchange_rate_input = ExchangeRatePLN.objects.create(
                            date=date,
                            currency=currency_input,
                            rate=Decimal(nbp_response.data["rates"][0]["mid"]),
                        )
                    else:
                        return nbp_response
                try:
                    exchange_rate_output = ExchangeRatePLN.objects.get(
                        date=date, currency=currency_output
                    )
                except ExchangeRatePLN.DoesNotExist:
                    nbp_response = NBP_API().get_exchange_response(
                        currency_output, date
                    )
                    if nbp_response.status_code == status.HTTP_200_OK:
                        exchange_rate_output = ExchangeRatePLN.objects.create(
                            date=date,
                            currency=currency_output,
                            rate=Decimal(nbp_response.data["rates"][0]["mid"]),
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
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#
