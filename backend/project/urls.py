from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from shop import api
from debug_toolbar.toolbar import debug_toolbar_urls

router = routers.DefaultRouter()
router.register("products", api.ProductViewSet)
router.register("orders", api.OrderViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
] + debug_toolbar_urls()
