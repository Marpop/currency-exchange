from django.urls import path

from apps.nbp.views import ExchangeRateView

urlpatterns = [
    path("nbp/", ExchangeRateView.as_view(), name="exchange"),
]
