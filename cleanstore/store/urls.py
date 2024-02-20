from django.urls import path
from .views import HomeViewSet, DashboardViewSet, ItemViewSet, OrderCreateView

urlpatterns = [
    path('', HomeViewSet.as_view({'get': 'list'}), name='home'),
    path('dashboard/', DashboardViewSet.as_view({'get': 'list'}), name='dashboard'),
    path('items/', ItemViewSet.as_view({'get': 'list', 'post': 'create'}), name='item-list-create'),
    path('orders/create/', OrderCreateView.as_view(), name='order-create'),  # Endpoint for creating orders
]
