from django.contrib import admin
from django.contrib.auth.models import User
from django.db.models import F, Sum, DecimalField
from django.db.models.functions import Coalesce
from . import models


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'description')
    list_filter = ('price',)
    search_fields = ('name', 'description')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'price')
        }),
        ('Additional Information', {
            'fields': ('description',),
            'classes': ('collapse',)
        }),
    )


class OrderLineInline(admin.TabularInline):
    model = models.OrderLine
    extra = 1
    raw_id_fields = ('product',)
    readonly_fields = ('line_total',)
    
    def line_total(self, obj):
        return obj.total if obj.id else "N/A"
    line_total.short_description = "Line Total"


class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'customer', 'display_total')
    inlines = [OrderLineInline]
    autocomplete_fields = ['customer']
    search_fields = ['customer__username', 'customer__email', 'customer__first_name', 'customer__last_name']
    list_filter = ('created_at', 'customer')
    
    fieldsets = (
        ('Customer Information', {
            'fields': ('customer', 'customer_received')
        }),
    )
    
    def display_total(self, obj):
        return obj.total
    display_total.short_description = "Total"

admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Order, OrderAdmin)

