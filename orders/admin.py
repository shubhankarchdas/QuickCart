from django.contrib import admin
from .models import Payment, Order, OrderProduct



class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    readonly_fields = ('payment', 'user', 'product', 'quantity', 'product_price', 'ordered')
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_number', 'full_name', 'phone', 'email', 'city', 'order_total', 'tax', 'status', 'is_ordered', 'created_at']
    list_filter = ['status', 'is_ordered']
    search_fields = ['order_number', 'first_name', 'last_name', 'phone', 'email']
    list_per_page = 20
    inlines = [OrderProductInline]

# @admin.register(Payment)
# class PaymentAdmin(admin.ModelAdmin):
#     list_display = ('id', 'user', 'payment_id', 'payment_method', 'amount_paid', 'status', 'created_at')
#     search_fields = ('payment_id', 'user__email', 'payment_method')
#     list_filter = ('status', 'payment_method', 'created_at')


# @admin.register(Order)
# class OrderAdmin(admin.ModelAdmin):
#     list_display = ('id', 'order_number', 'user', 'email', 'phone', 'order_total', 'tax', 'status', 'is_ordered', 'created_at')
#     list_display_links = ('order_number', 'user', 'email', 'phone')
#     list_filter = ('status', 'is_ordered', 'created_at')
#     search_fields = ('order_number', 'user__email', 'email', 'phone')
#     readonly_fields = ('order_number', 'order_total', 'tax', 'created_at', 'updated_at')
#     ordering = ('-created_at',)


# @admin.register(OrderProduct)
# class OrderProductAdmin(admin.ModelAdmin):
#     list_display = ('id', 'order', 'payment', 'user', 'product', 'quantity', 'product_price', 'ordered', 'created_at')
#     list_filter = ('ordered', 'created_at')
#     search_fields = ('order__order_number', 'user__email', 'product__product_name')
#     ordering = ('-created_at',)



admin.site.register(Payment)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)