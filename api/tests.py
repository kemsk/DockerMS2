from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
import json
from .models import Category, Item, Profile, Order, Review

class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        self.regular_user = User.objects.create_user(
            username='regular',
            email='regular@example.com',
            password='regularpassword'
        )
        self.client.force_authenticate(user=self.admin_user)
    
    def test_create_user(self):
        """Test creating a new user"""
        url = '/api/users/'
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
            'first_name': 'Test',
            'last_name': 'User'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.objects.get(username='testuser').email, 'test@example.com')
    
    def test_get_users(self):
        """Test retrieving a list of users"""
        url = '/api/users/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_get_user_detail(self):
        """Test retrieving a specific user"""
        url = f'/api/users/{self.regular_user.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'regular')


class CategoryTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)
        
        self.category = Category.objects.create(
            name='Test Category',
            description='Test Description'
        )
    
    def test_create_category(self):
        """Test creating a new category"""
        url = '/api/categories/'
        data = {
            'name': 'New Category',
            'description': 'New Description'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 2)
    
    def test_get_categories(self):
        """Test retrieving a list of categories"""
        url = '/api/categories/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_category_detail(self):
        """Test retrieving a specific category"""
        url = f'/api/categories/{self.category.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Category')


class ItemTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)
        
        self.category = Category.objects.create(
            name='Test Category',
            description='Test Description'
        )
        
        self.item = Item.objects.create(
            title='Test Item',
            description='Test Description',
            price=99.99,
            category=self.category,
            owner=self.user
        )
    
    def test_create_item(self):
        """Test creating a new item"""
        url = '/api/items/'
        data = {
            'title': 'New Item',
            'description': 'New Description',
            'price': 149.99,
            'category_id': self.category.id
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Item.objects.count(), 2)
    
    def test_get_items(self):
        """Test retrieving a list of items"""
        url = '/api/items/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_get_item_detail(self):
        """Test retrieving a specific item"""
        url = f'/api/items/{self.item.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Test Item')


class OrderTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.client.force_authenticate(user=self.user)
        
        self.category = Category.objects.create(
            name='Test Category',
            description='Test Description'
        )
        
        self.item = Item.objects.create(
            title='Test Item',
            description='Test Description',
            price=99.99,
            category=self.category,
            owner=self.user
        )
    
    def test_create_order(self):
        """Test creating a new order"""
        url = '/api/orders/'
        data = {
            'total_amount': 99.99,
            'shipping_address': '123 Test St',
            'payment_method': 'Credit Card',
            'items': [{
                'item_id': self.item.id,
                'quantity': 1,
                'price': 99.99
            }]
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 1)
    
    def test_get_orders(self):
        """Test retrieving a list of orders"""
        Order.objects.create(
            user=self.user,
            total_amount=99.99,
            shipping_address='123 Test St',
            payment_method='Credit Card'
        )
        url = '/api/orders/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
