from django.contrib import admin
from .models import Category, Product

admin.site.register(Category)
admin.site.register(Product)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category')

admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)
