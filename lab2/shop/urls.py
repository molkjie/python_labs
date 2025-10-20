from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_index, name='shop_index'),  # головна сторінка магазину
    path('categories/', views.category_list, name='category_list'),
    path('products/', views.product_list, name='product_list'),
]