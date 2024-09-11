from django.contrib import admin

from ecommerce.models import Customer, Product, Order, OrderItem, ShippingAddress

# Register your models here.
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
