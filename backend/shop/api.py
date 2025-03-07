from rest_framework import viewsets, permissions, status
from rest_framework.response import Response

from . import serializers
from . import models

class IsSuperAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow superadmins to edit products
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to superadmins
        return request.user and request.user.is_superuser

class ProductViewSet(viewsets.ModelViewSet):
    queryset = models.Product.objects.all()
    serializer_class = serializers.ProductSerializer
    permission_classes = [IsSuperAdminOrReadOnly]

class OrderViewSet(viewsets.ModelViewSet):
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """
        This view should return a list of all orders
        for the currently authenticated user, or all orders for superadmins.
        """
        if self.request.user.is_superuser:
            return models.Order.objects.all()
        return models.Order.objects.filter(customer=self.request.user)

class OrderLineViewSet(viewsets.ModelViewSet):
    queryset = models.OrderLine.objects.all()
    serializer_class = serializers.OrderLineSerializer

