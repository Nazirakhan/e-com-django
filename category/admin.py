from django.contrib import admin
from .models import Category
from django.utils.html import format_html

# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ('category_name','slug','display_image')

    def display_image(self, obj):  
        if obj.category_img:  
            return format_html('<img src="{}" width="50" />', obj.category_img.url)
        else:
            return 'No Image'

    display_image.short_description = 'Image Preview'
    

admin.site.register(Category,CategoryAdmin)