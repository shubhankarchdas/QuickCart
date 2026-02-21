from django.contrib import admin
from .models import Category

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('category_name',)}
    list_display = ('category_name', 'slug', 'description','is_featured', 'category_image')
    list_editable = ('is_featured',)
    list_display_links = ('category_name', 'slug')

admin.site.register(Category, CategoryAdmin)