from django.urls import path
from . import views


urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('admin-dashboard/', views.admin_dashboard, name='admin-dashboard'),
    path('', views.home, name='home'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('<int:pk>/edit/', views.OrderUpdateView.as_view(), name='order-edit'),
    path('<int:pk>/delete/', views.OrderDeleteView.as_view(), name='order-delete'),
]
