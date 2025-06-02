from django.urls import path
from . import views

urlpatterns = [
    path('orders/create/', views.OrderCreateView.as_view(), name='order_create'),
    path('orders/created/<int:order_id>/', views.OrderCreatedView.as_view(), name='order_created'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('my_orders/', views.UserOrdersView.as_view(), name='user_orders'),
]
