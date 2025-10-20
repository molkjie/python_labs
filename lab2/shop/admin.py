from django.contrib import admin
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_editable = ('slug',)    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category', 'slug')
    list_filter = ('category',)      # фільтрація по категорії
    list_editable = ('price',)       # дозволяє редагувати ціну без відкриття записи
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
