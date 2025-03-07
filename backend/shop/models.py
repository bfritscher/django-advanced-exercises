from django.db import models
from django.utils.functional import cached_property
from django.db.models import Sum, F, Prefetch, DecimalField
from django.db.models.functions import Coalesce

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    customer_received = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Order {self.id}"
    
    @cached_property
    def total(self):
        return sum([line.total for line in self.orderlines.all()])


class OrderLine(models.Model):
    product = models.ForeignKey(Product, related_name="orderlines", on_delete=models.CASCADE)
    order = models.ForeignKey("Order", related_name="orderlines", on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    @cached_property
    def total(self):
        """
        Calculate the total cost of this line item.
        Used in both admin and API serializers.
        """
        return self.product.price * self.quantity
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
