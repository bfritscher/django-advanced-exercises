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


class OrderManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related('customer').prefetch_related(
            Prefetch(
                'orderlines',
                queryset=OrderLine.objects.select_related('product')
            )
        ).annotate(
            total_price=Coalesce(
                Sum(F('orderlines__quantity') * F('orderlines__product__price')),
                0,
                output_field=DecimalField()
            )
        )


class Order(models.Model):
    objects = OrderManager()

    customer = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    customer_received = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return f"Order {self.id}"
    
    @property
    def total(self):
        """
        Return the total cost of the order.
        This uses the annotated total_price if available, 
        avoiding any additional database queries.
        Used in both admin and API serializers.
        """
        if hasattr(self, 'total_price'):
            return self.total_price
        
        # Fallback to database aggregation if not annotated
        result = self.orderlines.aggregate(
            total=Sum(F('quantity') * F('product__price'))
        )
        return result['total'] or 0


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
