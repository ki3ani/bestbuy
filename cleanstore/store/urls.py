from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.home, name='home'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('<int:pk>/edit/', views.OrderUpdateView.as_view(), name='order-edit'),
    path('<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order-delete'),
    path('items/<int:item_id>/', views.item_detail, name='item_detail'),
    path('create_order/<int:item_id>/', views.create_order, name='create_order'),
]
