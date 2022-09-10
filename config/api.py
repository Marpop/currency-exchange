from django.urls import include, path

urlpatterns = [path("nbp/", include(("apps.nbp.urls", "nbp")))]
