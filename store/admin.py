from django.contrib import admin
from .models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'is_available', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('product_name',)}
    list_filter = ('is_available', 'created_at', 'updated_at')
    search_fields = ('product_name', 'description')
    list_editable = ('price', 'stock', 'is_available')



admin.site.register(Product, ProductAdmin)