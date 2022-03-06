from unittest.mock import patch

from common.mocking import mock_make_request
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class TestUserApi(APITestCase):
    """
    Tests for User Authentication Apis
    """
    def client(self):
        return APIClient()

    @patch('userAuth.signals.make_request', return_value=mock_make_request)
    def add_default_user(self, mock_user_data_=None):
        user_data = {
            'username': 'test_admin',
            'password': 'Admin123@',
            'email': 'test@gmail.com'
        }  # just making it bulletproof
        response = self.client.post('/users/', data=user_data)
        return response.json()

    def jwt_headers(self):
        self.add_default_user()
        data = {
            "username": "test_admin",
            "password": "Admin123@"
        }
        response = self.client.post('/login/', data=data)
        response_data = response.json()
        jwt_token = response_data['access']
        return self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + jwt_token)

    def test_get_user_login_api_with_valid_data(self):
        """
        Test Login api with valid data.
        """
        self.add_default_user()
        data = {
            "username": "test_admin",
            "password": "Admin123@"
        }
        response = self.client.post('/login/', data=data)
        assert response.status_code == status.HTTP_200_OK

    def test_get_user_login_api_with_invalid_data(self):
        """
        Test Login api with Invalid data.
        """
        self.add_default_user()
        data = {
            "username": "wrong",
            "password": "wrong@"
        }
        response = self.client.post('/login/', data=data)
        response_data = response.json()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response_data['detail'] == 'No active account found with the given credentials'

    def test_get_user_register_api_with_invalid_data(self):
        """
        Test register api with Invalid data.
        """
        user_data = {'username': 'test_admin'}
        response = self.client.post('/users/', data=user_data)
        response_data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data['message'] == 'User Not Registered'

    @patch('userAuth.signals.make_request', return_value=mock_make_request)
    def test_get_user_register_api_with_valid_data(self, mock_user_data_):
        """
        Test register api with valid data.
        """
        user_data = {
            'username': 'test_admin',
            'password': 'Admin123@',
            'email': 'test@gmail.com'
        }
        response = self.client.post('/users/', data=user_data)
        response_data = response.json()
        assert response.status_code == status.HTTP_201_CREATED
        assert response_data['message'] == 'User Registered'

    def test_get_user_detail_api_without_authentication(self):
        """
        Test User Detail api without authentication.
        """
        self.add_default_user()
        response = self.client.get('/users/1/')
        response_data = response.json()
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response_data['detail'] == 'Authentication credentials were not provided.'

    def test_get_user_detail_api_with_authentication(self):
        """
        Test User Detail api without authentication.
        """
        response = self.client.get(f'/users/1/', headers=self.jwt_headers())
        response_data = response.json()
        assert response.status_code == status.HTTP_200_OK
        assert response_data['username'] == 'test_admin'
