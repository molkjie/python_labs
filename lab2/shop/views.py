from django.shortcuts import render
from .models import Product, Category

def index(request):
    products = Product.objects.all()
    return render(request, 'shop/index.html', {'products': products})
def shop_index(request):
    # можна показати коротку сторінку або останні товари
    products = Product.objects.all()[:5]
    return render(request, 'shop/product_list.html', {'products': products})

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'shop/category_list.html', {'categories': categories})

def product_list(request):
    products = Product.objects.select_related('category').all()
    return render(request, 'shop/product_list.html', {'products': products})
