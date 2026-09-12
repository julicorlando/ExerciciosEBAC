from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from .views import HealthView, hello, update_server

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/health/", HealthView.as_view(), name="health"),
    path("api/token/", obtain_auth_token, name="api-token"),
    path("api/", include("store.urls")),
    path("hello/", hello, name="hello"),
    path("update_server/", update_server, name="update-server"),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]
