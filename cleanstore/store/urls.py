from django.urls import path, include
from rest_framework import routers
from .views import HomeViewSet, DashboardViewSet, ItemViewSet, OrderViewSet

router = routers.DefaultRouter()
router.register(r'items', ItemViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('home/', HomeViewSet.as_view({'get': 'list'}), name='home'),
    path('dashboard/', DashboardViewSet.as_view({'get': 'list'}), name='dashboard'),
]
