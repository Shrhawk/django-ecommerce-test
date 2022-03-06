import datetime
import json

from common.custom_mixin import MixedPermissionModelViewSet
from common.external_apis_info import APIS_INFO
from common.request_helpers import make_request, _mutable
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response

from .serializers import UserModelSerializer, SwaggerUserModelSerializer


class UserViewSet(viewsets.ViewSet, MixedPermissionModelViewSet):
    """
    UserViewSet for creating/retrieving user
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserModelSerializer
    permission_classes_by_action = {
        'list': [IsAdminUser],
        'retrieve': [IsAuthenticated],
        'create': [AllowAny]
    }
    http_method_names = ['get', 'post', 'head']

    def list(self, request):
        queryset = get_user_model().objects.all()
        serializer_class = UserModelSerializer(queryset, many=True)
        return Response(serializer_class.data)

    def retrieve(self, request, pk=None):
        queryset = get_user_model().objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer_class = UserModelSerializer(post)
        return Response(serializer_class.data)

    @swagger_auto_schema(request_body=SwaggerUserModelSerializer)
    def create(self, request):
        user_data = request.data
        api_response = self.enrich_user_data(user_data)
        if not api_response:
            return Response({'message': 'User Not Registered'}, status=status.HTTP_400_BAD_REQUEST)
        user_data['user_ip'] = api_response['user_ip']
        user_data['holidays'] = json.dumps(api_response['holidays'])
        serializer_class = UserModelSerializer(data=user_data)
        if serializer_class.is_valid():
            password = serializer_class.validated_data.get('password')
            serializer_class.validated_data['password'] = make_password(password)
            serializer_class.save()
            return Response({'message': 'User Registered'}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {'message': 'User Not Registered', "Error": serializer_class.errors},
                status=status.HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def enrich_user_data(user_data):
        """
        enrich user data according to his/her Geolocation and Holidays
        And Validate Email
        """
        user_data = _mutable(user_data)

        email = user_data.get('email', '')
        if not email:
            return

        api_url = APIS_INFO['email_validation_api']
        data = {"email": email}
        email_validation = make_request(method='get', api_url=api_url, data=data, retries=3)
        if email_validation['data']['deliverability'] != 'DELIVERABLE':
            return

        api_url = APIS_INFO['geolocation_api']
        ip_address = make_request(method='get', api_url=api_url, retries=3)
        if not ip_address:
            return

        user_ip = ip_address['data']['ip_address']
        country_code = ip_address['data']['country_code']
        current_date = datetime.date.today()
        api_url = APIS_INFO['holidays_api']
        data = {
            "country": country_code,
            "year": current_date.year,
            "month": current_date.month,
            "day": current_date.day
        }
        holidays = make_request(method='get', api_url=api_url, data=data, retries=3)
        holidays = holidays.get('data', {})
        return {'user_ip': user_ip, 'holidays': holidays}
