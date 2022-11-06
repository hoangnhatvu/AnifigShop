from django.contrib import admin
from .models import Order, OrderItem, Payment

admin.site.register(Order)
admin.site.register(Payment)
admin.site.register(OrderItem)
