from django.contrib import admin
from .models import Item,Order,OrderItem,DiscountCode,OrderDiscount,Gallery

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','ordered']

admin.site.register(Item)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(DiscountCode)
admin.site.register(OrderDiscount)
admin.site.register(Gallery)
