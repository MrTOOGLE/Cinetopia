from django.urls import path
from . import views

urlpatterns = [
    path('shop/', views.ProductsListView.as_view(), name='shop'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/', views.cart_detail, name='cart_detail'),
]
