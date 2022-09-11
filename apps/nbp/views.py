from django.http import Http404

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
            nbp = NBP_API()
            response = nbp.exchange(date, currency_input, currency_output, amount)
            if response.status_code == status.HTTP_200_OK:
                return response
            if response.status_code in [
                status.HTTP_404_NOT_FOUND,
                status.HTTP_400_BAD_REQUEST,
            ]:
                raise Http404
            if response.status_code == status.HTTP_503_SERVICE_UNAVAILABLE:
                return Response(
                    {"detail": "Service unavailable."},
                    status=status.HTTP_503_SERVICE_UNAVAILABLE,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
