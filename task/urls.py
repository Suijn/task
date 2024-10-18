from django.contrib import admin
from django.urls import include, path

from task.apps.prefixes.views.urls import prefixes_router

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(prefixes_router.urls)),
]
