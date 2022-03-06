from common.custom_mixin import MixedPermissionModelViewSet
from common.request_helpers import _mutable
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .serializers import UserModelSerializer, SwaggerUserModelSerializer


class UserViewSet(viewsets.ViewSet, MixedPermissionModelViewSet):
    """
    UserViewSet for creating/retrieving user
    """
    queryset = get_user_model().objects.all()
    serializer_class = UserModelSerializer
    permission_classes_by_action = {
        'retrieve': [IsAuthenticated],
        'create': [AllowAny]
    }
    http_method_names = ['get', 'post', 'head']

    def list(self, request):
        serializer = []
        return Response(serializer)

    def retrieve(self, request, pk=None):
        queryset = get_user_model().objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer_class = UserModelSerializer(post)
        return Response(serializer_class.data)

    @swagger_auto_schema(request_body=SwaggerUserModelSerializer)
    def create(self, request):
        user_data = _mutable(request.data)
        user_data['user_ip'] = self.get_client_ip(request)
        serializer_class = UserModelSerializer(data=user_data)
        if serializer_class.is_valid():
            password = serializer_class.validated_data.get('password')
            serializer_class.validated_data['password'] = make_password(password)
            serializer_class.save()
            return Response({'message': 'User Registered'}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {
                    'message': 'User Not Registered',
                    "Error": serializer_class.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

    @staticmethod
    def get_client_ip(request):
        """
        get client ip from request
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
