from .models import User, LogRequests
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.validators import UniqueValidator
from django.contrib.auth import authenticate
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    arn_number = serializers.CharField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'first_name', 'last_name', 'arn_number', 'is_staff', 'is_superuser']

    def create(self, validated_data):
        if not 'first_name' in validated_data:
            raise serializers.ValidationError('First Name Not Given.')
        
        user = User.objects.create_user(**validated_data)
        return user


class LoginJWTSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        # Authenticate the user
        user = authenticate(request=None, email=email, password=password)

        if user is None:
            raise serializers.ValidationError('Invalid email or password.')

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
    
class LogRequestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LogRequests
        fields = ['id', 'url', 'method', 'request_payload', 'response_payload', 'status_code', 'timestamp', 'success']
