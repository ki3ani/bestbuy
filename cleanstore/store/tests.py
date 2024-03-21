from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate
from store.models import Customer, Item, Order
from store.views import HomeViewSet, DashboardViewSet, ItemViewSet, OrderViewSet
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase

class HomeViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()


    def test_list_authenticated_user(self):
        user = User.objects.create(username='testuser')
        client = APIClient()
        client.force_authenticate(user=user)

        request = self.factory.get('/home/')
        view = HomeViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, 200)

    def test_list_unauthenticated_user(self):
        request = self.factory.get('/home/')
        view = HomeViewSet.as_view({'get': 'list'})
        response = view(request)

        self.assertEqual(response.status_code, 200)

class DashboardViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_superuser(username='admin', email='mungai.kenneth@strathmore.edu', password='omniman2024')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


class ItemViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.admin_user = User.objects.create_superuser(username='admin', email='mungai.kenneth@strathmore.edu', password='omniman2024')
        self.non_admin_user = User.objects.create(username='user')
        self.client = APIClient()

    def test_list(self):
        request = self.factory.get('/items/')
        force_authenticate(request, user=self.admin_user)
        view = ItemViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_create_as_admin(self):
        data = {'name': 'New Item'}  # Missing 'in_stock' and 'price'
        request = self.factory.post('/items/', data, format='json')
        force_authenticate(request, user=self.admin_user)
        view = ItemViewSet.as_view({'post': 'create'})
        response = view(request)
        self.assertEqual(response.status_code, 400)  # Expect Bad Request

    def test_create_as_non_admin(self):
        # Implement test case for creating item as non-admin user
        pass

    def test_update_as_admin(self):
        item = Item.objects.create(name='Test Item', in_stock=True, price=10.00)
        data = {'name': 'Updated Item', 'in_stock': False, 'price': 20.00}
        request = self.factory.put(f'/items/{item.pk}/', data, format='json')
        force_authenticate(request, user=self.admin_user)
        view = ItemViewSet.as_view({'put': 'update'})
        response = view(request, pk=item.pk)
        self.assertEqual(response.status_code, 400)  # Expect Bad Request

class OrderViewSetTestCase(APITestCase):
    def setUp(self):
        # Set up necessary objects for the tests
        self.factory = APIRequestFactory()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='omniman2024'
        )
        self.normal_user = User.objects.create_user(
            username='normal_user',
            email='normal@example.com',
            password='testpassword'
        )
        self.item = Item.objects.create(
            name='Test Item',
            in_stock=True,
            price=10.00
        )

    def test_create_order_as_admin(self):
        # Ensure creating an order as an admin user returns 403 Forbidden
        url = reverse('order-list')
        data = {'item': self.item.pk, 'quantity': 1}
        request = self.factory.post(url, data, format='json')
        request.user = self.admin_user
        view = OrderViewSet.as_view({'post': 'create'})
        response = view(request)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
