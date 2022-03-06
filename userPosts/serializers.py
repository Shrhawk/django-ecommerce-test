from rest_framework import serializers
from userAuth.serializers import UserModelSerializer

from .models import Post, PostLikes


class PostModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer()

    class Meta:
        model = Post
        fields = ('id', 'content', 'user')


class CreatePostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'content', 'user')


class SwaggerPostModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('id', 'content')


class PostLikeModelSerializer(serializers.ModelSerializer):
    user = UserModelSerializer()
    post = PostModelSerializer()

    class Meta:
        model = PostLikes
        fields = ('id', 'post', 'user')


class CreatePostLikeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLikes
        fields = ('id', 'post', 'user')
        
        
class SwaggerPostLikeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLikes
        fields = ('id', 'post')
