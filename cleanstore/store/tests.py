from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate
from store.models import Item, Order
from store.views import HomeViewSet, DashboardViewSet, ItemViewSet, OrderViewSet
from rest_framework.test import APITestCase


class HomeViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_list(self):
        request = self.factory.get('/home/')
        view = HomeViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

class DashboardViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='testuser')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list(self):
        request = self.factory.get('/dashboard/')
        request.user = self.user
        view = DashboardViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

class ItemViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin_user = User.objects.create(username='admin', is_staff=True)
        self.non_admin_user = User.objects.create(username='user', is_staff=False)
        self.client = APIClient()

    def test_list(self):
        request = self.factory.get('/items/')
        force_authenticate(request, user=self.admin_user)  
        view = ItemViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_create_as_admin(self):
        data = {'name': 'New Item', 'in_stock': True, 'price': 15.00}
        request = self.factory.post('/items/', data, format='json')
        force_authenticate(request, user=self.admin_user)
        view = ItemViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 201)

    def test_create_as_non_admin(self):
        data = {'name': 'New Item', 'in_stock': True, 'price': 15.00}
        request = self.factory.post('/items/', data, format='json')
        force_authenticate(request, user=self.non_admin_user)
        view = ItemViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 403)


class OrderViewSetTestCase(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create(username='testuser')
        self.client.force_authenticate(user=self.user)

        # Populate the database with an item
        self.item = Item.objects.create(name='Test Item', in_stock=True, price=10.00)

    def test_list(self):
        request = self.factory.get('/orders/')
        request.user = self.user
        view = OrderViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
