from django.contrib import admin
from .models import Account
from Orders.models import OrderProduct
from django.contrib.auth.admin import UserAdmin

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


admin.site.register(Account, AccountAdmin)