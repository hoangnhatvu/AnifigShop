from django.contrib import admin
from .models import Order, OrderProduct, Payment

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'order_total', 'is_ordered')
    
class OrderProductAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'user')

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct, OrderProductAdmin)
