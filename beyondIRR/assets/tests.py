from .models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .arn_verification import check_arn
from rest_framework_simplejwt.tokens import RefreshToken

class UserTestCase(APITestCase):
    def setUp(self):
        self.url = reverse('signup')
        self.user1 = {
            "email": "user1@example.com",
            "password": "testpassword123",
            "arn_number": 54321,
            "first_name": "Test",
        }
        
        self.user2 = {
            "email": "tnageshgupta@yahoo.com",
            "password": "testpassword123",
            "arn_number": 87216,
            "first_name": "Test",
            "last_name": "User"    
        }
        
        self.user3 = {
            "email": '',
            "password": 'testpassword123',
            "arn_number": 69,
            "first_name": 'Test',
            "last_name": 'User'
        }
        
        self.response1 = self.client.post(self.url, self.user1, format='json').json()
        self.response2 = self.client.post(self.url, self.user2, format='json').json()
        self.response3 = self.client.post(self.url, self.user3, format='json').json()
        self.response4 = self.client.post(self.url, self.user2, format='json').json()
        
    def test_invalid_arn(self):
        res1 = check_arn(self.user1['arn_number'])
        res2 = check_arn(self.user2['arn_number'])
        res3 = check_arn(self.user3['arn_number'])
        self.assertEqual(type(res1), str)
        self.assertEqual(type(res2), dict)
        self.assertNotEqual(type(res3), str)

    def test_valid_email_for_amfi(self):
        res2 = check_arn(self.user2['arn_number'])
        res3 = check_arn(self.user3['arn_number'])
        self.assertEqual(res2['amfi_email'], self.user2['email'])
        self.assertEqual(res3['amfi_email'], '')

    def test_signup_missing_fields(self):
        self.assertEqual(self.response1['status'], status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.response3['status'], status.HTTP_400_BAD_REQUEST)

    def  test_signup_success(self):
        self.assertEqual(self.response2['status'], status.HTTP_201_CREATED)
        self.assertEqual(self.response2['message'], 'User created successfully')

    def test_user_exist(self):
        self.assertNotEqual(self.response4['status'], status.HTTP_201_CREATED)

class LoginTests(APITestCase):
    def setUp(self):
        self.login = reverse('login')
        self.signup = reverse('signup')
        
        self.credentials1 = {
            "email": "tnageshgupta@yahoo.com",
            "password": "testpassword123"
        }
        self.credentials2 = {
            "email": "admin@example.com",
            "password": "Test@123"
        }
        
        self.user2 = {
            "email": "tnageshgupta@yahoo.com",
            "password": "testpassword123",
            "arn_number": 87216,
            "first_name": "Test",
            "last_name": "User"    
        }
        
        self.response2 = self.client.post(self.signup, self.user2, format='json').json()

    def test_login_success(self):
        response1 = self.client.post(self.login, self.credentials1, format='json')
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertIn('access', response1.json())

    def test_login_failure(self):
        response2 = self.client.post(self.login, self.credentials2, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn('access', response2.json())

class AllUsersTests(APITestCase):
    def setUp(self):
        self.url = reverse('users')

        self.user = User.objects.create(email="user@example.com", password="Test@123", arn_number=54321, first_name="Test")
        self.admin = User.objects.create(email="admin@example.com", password="Test@123", arn_number=12345, first_name="Test", is_superuser=True, is_staff=True)
        
        self.admin_token = self.get_jwt_token(self.admin)
        self.user_token = self.get_jwt_token(self.user) 
          
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    

    def test_get_all_users(self):
        # print(self.admin_token)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.json()), list)

    def test_unauthorized_access(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
class CurrentUserTests(APITestCase):
    def setUp(self):
        self.url = reverse('curr-list')
        self.user = User.objects.create(email="user@example.com", password="Test@123", arn_number=54321, first_name="Test")
        self.user_token = self.get_jwt_token(self.user) 
          
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_current_user(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user_email', response.json())

    def test_unauthorized_access(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('user_email', response.json())


class LogViewTests(APITestCase):
    def setUp(self):
        self.url = reverse('log-list')

        self.user = User.objects.create(email="user@example.com", password="Test@123", arn_number=54321, first_name="Test")
        self.admin = User.objects.create(email="admin@example.com", password="Test@123", arn_number=12345, first_name="Test", is_superuser=True, is_staff=True)
        
        self.admin_token = self.get_jwt_token(self.admin)
        self.user_token = self.get_jwt_token(self.user) 
          
    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    def test_get_logs(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.admin_token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(type(response.json()), list)

    def test_unauthorized_access(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.user_token)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)