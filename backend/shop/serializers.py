from rest_framework import serializers
from django.contrib.auth import models as auth

from . import models

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = "__all__"


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = auth.User
        fields = ["id", "username", "email", "first_name", "last_name"]


class OrderLineSerializer(serializers.ModelSerializer):
    total = serializers.SerializerMethodField()
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = models.OrderLine
        fields = "__all__"
    
    def get_total(self, obj):
        return obj.total


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    total = serializers.SerializerMethodField()
    orderlines = OrderLineSerializer(many=True, read_only=True)
    
    class Meta:
        model = models.Order
        fields = "__all__"
    
    def get_total(self, obj):
        return obj.total
