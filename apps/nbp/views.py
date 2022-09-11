from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.nbp.serializers import ExchangeRateSerializer
from apps.nbp.services import NBP_API


class ExchangeRateView(APIView):
    @extend_schema(parameters=[ExchangeRateSerializer])
    def get(self, request) -> Response:
        serializer = ExchangeRateSerializer(data=request.query_params)
        if serializer.is_valid():
            date = serializer.validated_data["date"]
            currency_input = serializer.validated_data["currency_input"]
            currency_output = serializer.validated_data["currency_output"]
            amount = serializer.validated_data["amount"]
            nbp_exchange = NBP_API().exchange(
                date, currency_input, currency_output, amount
            )
            return Response({currency_output: nbp_exchange}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
