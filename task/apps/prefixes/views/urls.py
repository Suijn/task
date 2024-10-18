from rest_framework import routers

from task.apps.prefixes.views.views import PrefixViewSet

prefixes_router = routers.DefaultRouter()
prefixes_router.register(r"prefixes", PrefixViewSet, basename="prefix")
