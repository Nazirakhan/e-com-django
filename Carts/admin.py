from django.contrib import admin
from .models import Cart, CartItem
from store.models import Product

# Register your models here.

class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id','date_added')

class CartItemAdmin(admin.ModelAdmin):
    list_display= ('get_product_name','quantity', 'cart', 'is_active')

    def get_product_name(self, obj):
        return obj.product.product_name if obj.product else None
    get_product_name.short_description = 'Product Name'

admin.site.register(Cart,CartAdmin)
admin.site.register(CartItem, CartItemAdmin)