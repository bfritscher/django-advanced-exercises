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


class OrderAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Order, OrderAdmin)

