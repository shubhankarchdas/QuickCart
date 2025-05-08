from django.contrib import admin
from .models import Product, Variation
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'is_available', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('product_name',)}
    list_filter = ('is_available', 'created_at', 'updated_at')
    search_fields = ('product_name', 'description')
    list_editable = ('price', 'stock', 'is_available')


class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active', 'created_at', 'updated_at')
    search_fields = ('product__product_name', 'variation_category', 'variation_value')
    list_editable = ('is_active',)

admin.site.register(Product, ProductAdmin)
admin.site.register(Variation, VariationAdmin)