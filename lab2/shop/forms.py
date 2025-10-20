# shop/forms.py
from django import forms
from .models import Category, Product

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'slug']  

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'category', 'description', 'slug']  
