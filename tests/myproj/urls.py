from django.apps import apps
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("pyhub-components/", include("pyhub_components.urls")),
]

# check app install
if apps.is_installed("debug_toolbar"):
    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]
