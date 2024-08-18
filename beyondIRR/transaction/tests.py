from django.test import TestCase
from rest_framework.test import APITestCase
from .models import User, Transaction
from django.urls import reverse
from rest_framework import status
import random
import datetime
from django.utils import timezone
from beyondIRR.settings import BASE_DIR
from rest_framework_simplejwt.tokens import RefreshToken

class AddTransactionViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('upload-transaction')
        self.valid_file_path = str(BASE_DIR) + '/template.xlsx'
        self.invalid_file_path = str(BASE_DIR) + '/public_key.pem'
        self.missing_values_file_path = str(BASE_DIR) + '/missing_values.xlsx'

        self.user = User.objects.create(email="user@example.com", password="Test@123", arn_number=54321, first_name="Test")
        self.user_token = self.get_jwt_token(self.user) 
          
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_add_transaction_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        with open(self.valid_file_path, 'rb') as file:
            response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)

    def test_add_transaction_invalid_file(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        with open(self.invalid_file_path, 'rb') as file:
            response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
        
    def test_add_transaction_missing_values_file(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        with open(self.missing_values_file_path, 'rb') as file:
            response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)


    def test_unauthorized_access(self):
        with open(self.valid_file_path, 'rb') as file:
            response = self.client.post(self.url, {'file': file}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UpdateTransactionViewTest(APITestCase):
    def setUp(self):
        self.url = reverse('view-transaction')
        self.user = User.objects.create(email="user@example.com", password="Test@123", arn_number=54321, first_name="Test")
        self.user_token = self.get_jwt_token(self.user) 
        
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def update_transactions(self, user, product, asset_class, date, unit, amount):
        date = datetime.datetime.strptime(date, "%Y-%m-%d")  
        transaction = Transaction(
            user=user,
            product=product,
            asset_class=asset_class,
            date_of_transaction=date,
            units=unit,
            amount=amount
        )
        return transaction
        
    def test_update_transaction(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.get(self.url)
        transaction1 = self.update_transactions(self.user, 'PRODUCT__1', "EQUITY", "2024-1-23", 10, 1000)
        transaction2 = self.update_transactions(self.user, 'PRODUCT__1', "EQUITY", "2024-1-23", 10, 2000)
        transaction1.save()
        transaction2.save()
        count = Transaction.objects.filter(product='PRODUCT__1', date_of_transaction='2024-1-23').count()
        self.assertEqual(transaction1.amount, 1000)
        self.assertEqual(transaction2.amount, 2000)
        self.assertEqual(count, 2)
        
class TransactionsViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('view-transaction')
        self.user = User.objects.create(email="user@example.com", password="Test@123", arn_number=54321, first_name="Test")
        self.user_token = self.get_jwt_token(self.user) 
        self.dummy_transactions(self.user)
        
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def dummy_transactions(self, user):
        asset_classes = ['Equity', 'Debt', 'Alternate']
        products = ['PRODUCT_001', 'PRODUCT_002', 'PRODUCT_004', 'PRODUCT_005']
        
        for _ in range(10):  
            amount = round(random.uniform(-10000.0, 10000.0), 2)  
            unit = round(random.uniform(-100.0, 100.0), 2)  
            year = random.randint(2020, 2026)
            day = random.randint(1, 28)
            month = random.randint(1, 12)
            asset_class = random.choice(asset_classes)
            product = random.choice(products)
            date = datetime.datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")  
            Transaction.objects.create(
                user=user,
                product=product,
                asset_class=asset_class,
                date_of_transaction=date,
                units=unit,
                amount=amount
            )
            
    def test_view_transactions(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('success', response.data)

    def test_unauthorized_access(self):
        response = self.client.get(self.url)        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class SummaryTests(APITestCase):
    def setUp(self):
        self.url = reverse('summary')
        self.user = User.objects.create(email="user@example.com", password="Test@123", arn_number=54321, first_name="Test")
        self.user_token = self.get_jwt_token(self.user) 
        self.dummy_transactions(self.user)
        
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def dummy_transactions(self, user):
        asset_classes = ['Equity', 'Debt', 'Alternate']
        products = ['PRODUCT_001', 'PRODUCT_002', 'PRODUCT_004', 'PRODUCT_005']
        
        for _ in range(10):  
            amount = round(random.uniform(-10000.0, 10000.0), 2)  
            unit = round(random.uniform(-100.0, 100.0), 2)  
            year = random.randint(2020, 2026)
            day = random.randint(1, 28)
            month = random.randint(1, 12)
            asset_class = random.choice(asset_classes)
            product = random.choice(products)
            date = datetime.datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")  
            Transaction.objects.create(
                user=user,
                product=product,
                asset_class=asset_class,
                date_of_transaction=date,
                units=unit,
                amount=amount
            )
    def test_get_summary(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('success', response.data)

    def test_unauthorized_access(self):
        response = self.client.get(self.url)        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
