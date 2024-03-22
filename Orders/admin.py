from django.contrib import admin
from .models import Payment, OrderProduct, Order

# Register your models here.
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_number","first_name","total","tax","order_total","phone","email","country","state","city","zip_code",)


admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)