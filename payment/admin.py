from django.contrib import admin
from .models import ShippingAddress,Order,OrderItem
from django.contrib.auth.models import User


# Register The model on the admin section thing
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)
# Create OrderItemInline

class OrderItemInline(admin.StackedInline):
    model=OrderItem
    extra=0
#extend our Order Model
class OrderAdmin(admin.ModelAdmin):
    model=Order
    readonly_fields=["date_ordered"]
    inlines=[OrderItemInline]     
#unregiter order Model
admin.site.unregister(Order)

#Re-Register Our Order and  OrderItems
admin.site.register(Order,OrderAdmin)    
    
