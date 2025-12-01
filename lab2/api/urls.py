from django.urls import path
from .views import (
    ProductListCreateView, ProductRetrieveUpdateDestroyView,
    CategoryListCreateView, CategoryRetrieveUpdateDestroyView
)

urlpatterns = [
    path('products/', ProductListCreateView.as_view(), name='api_product_list'),
    path('products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='api_product_detail'),
    path('categories/', CategoryListCreateView.as_view(), name='api_category_list'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view(), name='api_category_detail'),
]
