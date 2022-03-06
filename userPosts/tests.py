from unittest.mock import patch

from common.mocking import mock_make_request
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class TestPostApi(APITestCase):
    """
    Tests for Post Apis
    """
    def client(self):
        return APIClient()

    @patch('userAuth.views.make_request', return_value=mock_make_request)
    def add_default_user(self, mock_make_request_):
        # just making it bulletproof
        user_data = {
            'username': 'test_admin',
            'password': 'Admin123@',
            'email': 'test@gmail.com'
        }
        response = self.client.post('/users/', data=user_data)
        return response.json()

    def add_default_post(self):
        # just making it bulletproof
        user_data = {
            'user': '1',
            'content': 'hello there',
        }
        response = self.client.post('/posts/', data=user_data, headers=self.jwt_headers())
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

    def test_get_post_api_without_authentication(self):
        """
        Test post api without authentication.
        """
        response = self.client.get('/posts/1/')
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_get_post_api_with_authentication(self):
        """
        Test post api with authentication.
        """
        self.add_default_post()
        response = self.client.get('/posts/1/', headers=self.jwt_headers())
        assert response.status_code == status.HTTP_200_OK

    def test_get_post_api_with_valid_data(self):
        """
        Test post api with valid data.
        """
        self.add_default_post()
        response = self.client.get('/posts/1/', headers=self.jwt_headers())
        assert response.status_code == status.HTTP_200_OK

    def test_get_post_api_with_invalid_id(self):
        """
        Test post api with Invalid id.
        """
        self.add_default_post()
        response = self.client.get('/posts/999/', headers=self.jwt_headers())
        request_data = response.json()
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert request_data['detail'] == 'Not found.'

    def test_post_post_api_with_valid_data(self):
        """
        Test post api with Invalid id.
        """
        self.add_default_user()
        self.add_default_post()
        data = {
            'user': '1',
            'content': 'hello there 1'
        }
        response = self.client.post('/posts/', data=data, headers=self.jwt_headers())
        assert response.status_code == status.HTTP_201_CREATED

    def test_post_post_api_with_invalid_data(self):
        """
        Test post api with Invalid id.
        """
        self.add_default_user()
        self.add_default_post()
        response = self.client.post('/posts/', data={}, headers=self.jwt_headers())
        request_data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert request_data['massage']['content'] == ['This field is required.']

    def test_post_post_like_api_with_invalid_data(self):
        """
        Test post like api with Invalid user and post id.
        """
        data = {}
        response = self.client.post('/posts_like/', data=data, headers=self.jwt_headers())
        response_data = response.json()
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response_data['massage']['post'] == ['This field is required.']

    def test_post_post_like_api_with_valid_data(self):
        """
        Test post like api with valid user and post id.
        """
        self.add_default_user()
        self.add_default_post()
        data = {'user': 1, 'post': 1}
        response = self.client.post('/posts_like/', data=data, headers=self.jwt_headers())
        assert response.status_code == status.HTTP_201_CREATED
