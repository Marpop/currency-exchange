from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

urlpatterns = [path(settings.ADMIN_URL, admin.site.urls)] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)  # type: ignore

# API URLS
urlpatterns += [
    # API base url
    path("api/", include("config.api_router")),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),  # type: ignore
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),  # type: ignore
]

if settings.DEBUG and "debug_toolbar" in settings.INSTALLED_APPS:
    import debug_toolbar

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
