from django.contrib import admin
from .models import Cart, CartItem
from store.models import Product

# Register your models here.

class CartItemAdmin(admin.ModelAdmin):
    list_display= ('get_product_name','quantity', 'cart', 'is_active')

    def get_product_name(self, obj):
        return obj.product.product_name if obj.product else None
    get_product_name.short_description = 'Product Name'

admin.site.register(Cart)
admin.site.register(CartItem, CartItemAdmin)