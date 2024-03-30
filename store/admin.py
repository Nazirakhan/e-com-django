from django.contrib import admin
from .models import Product,Variation, ReviewRatings
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


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product','variation_category','variation_value','created_date','is_active')
    list_editable = ('is_active',)
    list_filter = ('product','variation_category','variation_value')

class ReviewRatingsAdmin(admin.ModelAdmin):
    list_display = ('product','user','rating','created_at')

admin.site.register(Product,ProductAdmin)
admin.site.register(Variation,VariationAdmin)
admin.site.register(ReviewRatings,ReviewRatingsAdmin)