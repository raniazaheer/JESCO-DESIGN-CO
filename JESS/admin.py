from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Customer, Product, Order, ShippingAdddress, Contact, users, OrderItem

# Register your models here.


# class showproducts(admin.ModelAdmin):
#     list_display = ['id', 'product_name', 'product_price',
#                     'product_image1', 'product_date']

# admin.site.register(models.Product, showproducts)
admin.site.register(users)

admin.site.register(Customer)
admin.site.register(OrderItem)


@admin.register(Contact)
class ContactModelAdmin(admin.ModelAdmin):
    list_display = [
        'subject', 'message'
    ]


@admin.register(Order)
class OrderModelAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'user', 'date_ordered', 'complete', 'transaction_id', 'delivery'
    ]


admin.site.register(ShippingAdddress)
# admin.site.register(Order)


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'product_price',
                    'product_image1', 'brand',  'category']


# @admin.register(Order)
# class OrderModelAdmin(admin.ModelAdmin):
    # list_display = ['id', 'user', 'customer',
    #                 'product', 'quantity', 'date_ordered', 'status']
