from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.shop_index, name='shop_index'),  # головна сторінка магазину
    path('categories/', views.category_list, name='category_list'),
    path('products/', views.product_list, name='product_list'),

    
    path('categories/page/', views.paginated_category_list, name='paginated_category_list'),
    path('products/page/', views.paginated_product_list, name='paginated_product_list'),

  
    path('products/create/', views.product_create, name='product_create'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),
    path('products/<int:pk>/update/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    
    path('categories/create/', views.category_create, name='category_create'),
    path('categories/<int:pk>/', views.category_detail, name='category_detail'),
    path('categories/<int:pk>/update/', views.category_update, name='category_update'),
    path('categories/<int:pk>/delete/', views.category_delete, name='category_delete'),
]
