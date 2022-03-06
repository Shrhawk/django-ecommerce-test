from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserModelSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        lower_email = value.lower()
        if get_user_model().objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("Email Already Exists")
        return lower_email

    class Meta:
        model = get_user_model()
        fields = ["username", "password", "first_name", "last_name", "email", "user_ip", "holidays"]
        
        
class SwaggerUserModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ["username", "password", "first_name", "last_name", "email"]
