from django.contrib import admin
from .models import Account, ProfileUser
from Orders.models import OrderProduct
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

# Register your models here.
class UserProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment','product','quantity','product_price','ordered',)
    extra = 0

class AccountAdmin(UserAdmin):
    list_display = ('email','first_name','last_name','username','last_login','date_joined','is_active')
    list_display_links = ('email','first_name')
    readonly_fields = ('last_login','date_joined')
    ordering = ('-date_joined',)
    inlines = [UserProductInline]

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class ProfileUserAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        if object.profile_picture:
            return format_html('<img src="{}" width="30" style="border-radius: 20%;" />'.format(object.profile_picture.url))
        else:
            return "No image available"
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail','user','city','state','country')

admin.site.register(Account, AccountAdmin)
admin.site.register(ProfileUser, ProfileUserAdmin)
