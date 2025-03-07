from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from . import serializers
from . import models


class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer


class OrderLineViewSet(viewsets.ModelViewSet):
    queryset = models.OrderLine.objects.all()
    serializer_class = serializers.OrderLineSerializer

