from django.contrib import admin
from .models import Payment,Order,OrderProduct


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user','created_at']


admin.site.register(Payment)
admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct)