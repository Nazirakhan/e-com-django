from django.contrib import admin
from .models import Product
from django.utils.html import format_html
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','display_image','created_date','modified_date','is_available', )
    prepopulated_fields = {'slug':('product_name',)}

    def display_image(self,obj):
        if obj.images:
            return format_html('<img src="{}" width="50" />', obj.images.url)
        else:
            return 'No Image'
    display_image.short_description = 'Image Preview'    
admin.site.register(Product,ProductAdmin)