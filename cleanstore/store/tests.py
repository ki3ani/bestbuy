from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory, APIClient, force_authenticate
from store.models import Customer, Item
from store.views import HomeViewSet, DashboardViewSet, ItemViewSet, OrderViewSet
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APIClient
from store.models import Item, Customer
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

class HomeViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()

    def test_list(self):
        request = self.factory.get('/home/')
        view = HomeViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_empty_stock(self):
        Item.objects.create(name='Out of Stock Item', in_stock=False, price=10.00)
        request = self.factory.get('/home/')
        view = HomeViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

class DashboardViewSetTestCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_superuser(username='admin', email='mungai.kenneth@strathmore.edu', password='omniman2024')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list(self):
        request = self.factory.get('/dashboard/')
        request.user = self.user
        view = DashboardViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_no_orders(self):
        request = self.factory.get('/dashboard/')
        request.user = self.user
        view = DashboardViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

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

    def test_update_as_admin(self):
        item = Item.objects.create(name='Test Item', in_stock=True, price=10.00)
        data = {'name': 'Updated Item', 'in_stock': False, 'price': 20.00}
        request = self.factory.put(f'/items/{item.pk}/', data, format='json')
        force_authenticate(request, user=self.admin_user)
        view = ItemViewSet.as_view({'put': 'update'})
        response = view(request, pk=item.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Item.objects.get(pk=item.pk).name, 'Updated Item')


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

        print(f"Admin Response Status Code: {response.status_code}")
        if response.status_code != status.HTTP_403_FORBIDDEN:
            print("Admin Response Data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_order_as_normal_user(self):
        # Ensure creating an order as a regular user returns 201 Created
        url = reverse('order-list')
        data = {'item': self.item.pk, 'quantity': 1}
        request = self.factory.post(url, data, format='json')
        request.user = self.normal_user
        view = OrderViewSet.as_view({'post': 'create'})
        response = view(request)

        print(f"Normal User Response Status Code: {response.status_code}")
        if response.status_code != status.HTTP_201_CREATED:
            print("Normal User Response Data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



def test_add_phone_number(self):
    user = User.objects.create(username='testuser')
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post('/add_phone_number/', {'phone_number': '+254701872345'}, format='json')
    self.assertEqual(response.status_code, 200)
    customer = Customer.objects.get(user=user)
    self.assertIsNotNone(customer.phone_number)
    self.assertEqual(customer.phone_number, '+254701872345')
