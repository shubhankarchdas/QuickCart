from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/<slug:category_slug>/', views.home, name='products_by_category'),
    # path('products/', views.product_list, name='product_list'),
    # path('products/<int:product_id>/', views.product_detail, name='product_detail'),
    # path('cart/', views.cart, name='cart'),
    # path('checkout/', views.checkout, name='checkout'),
]