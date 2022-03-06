from common.request_helpers import _mutable, get_current_user
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Post, PostLikes
from .serializers import (
    PostModelSerializer,
    CreatePostModelSerializer,
    PostLikeModelSerializer,
    CreatePostLikeModelSerializer,
    SwaggerPostModelSerializer,
    SwaggerPostLikeModelSerializer
)


@permission_classes([IsAuthenticated])
class PostViewSet(viewsets.ViewSet):
    """
    PostViewSet for listing or retrieving Posts.
    """
    def list(self, request):
        queryset = Post.objects.all()
        serializer = PostModelSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostModelSerializer(post)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=SwaggerPostModelSerializer)
    def create(self, request):
        user_data = _mutable(request.data)
        user_data['user'] = int(get_current_user(request))
        serializer = CreatePostModelSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Post saved successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({"massage": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(request_body=SwaggerPostModelSerializer)
    def update(self, request, pk=None):
        user_data = _mutable(request.data)
        current_user = int(get_current_user(request))
        check_post = Post.objects.filter(
            pk=pk,
            user=current_user,
            is_active=True
        ).update(content=user_data['content'])
        if check_post:
            return Response({'msg': 'Post updated successfully'}, status=status.HTTP_201_CREATED)
        return Response({"massage": 'Post not found'}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        try:
            request.data = _mutable(request.data)
        except:
            pass
        current_user = int(get_current_user(request))
        del_post = Post.objects.filter(
            pk=pk,
            user=current_user,
            is_active=True
        ).update(is_active=False)
        if del_post:
            return Response({'message': 'Post deleted successfully'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': "Can't delete post"}, status=status.HTTP_404_NOT_FOUND)


@permission_classes([IsAuthenticated])
class PostLikeViewSet(viewsets.ViewSet):
    """
    PostLikeViewSet for listing or retrieving postLikes.
    """
    def list(self, request):
        queryset = PostLikes.objects.all()
        serializer = PostLikeModelSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = PostLikes.objects.all()
        post = get_object_or_404(queryset, pk=pk)
        serializer = PostLikeModelSerializer(post)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=SwaggerPostLikeModelSerializer)
    def create(self, request):
        user_data = _mutable(request.data)
        user_data['user'] = int(get_current_user(request))
        like_check = self.dislike_if_liked_already(user_data)
        if like_check:
            return Response({'massage': 'User already liked this post'}, status=status.HTTP_401_UNAUTHORIZED)
        if user_data.get('post'):
            post_exists = self.post_exists_check(user_data)
            if not post_exists:
                return Response({'massage': 'Post does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = CreatePostLikeModelSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'massage': 'Post liked saved successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({"massage": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def dislike_if_liked_already(user_data):
        check_like = PostLikes.objects.filter(
            user=user_data.get('user'),
            post=user_data.get('post')
        ).update(is_active=False)
        return True if check_like else False

    @staticmethod
    def post_exists_check(user_data):
        user_data = _mutable(user_data)
        exists = Post.objects.filter(
            id=user_data.get('post')
        )
        return True if exists else False
