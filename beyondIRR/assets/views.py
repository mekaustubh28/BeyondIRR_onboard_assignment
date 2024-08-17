from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, LoginJWTSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.exceptions import ValidationError

# Create your views here.
class SignUp(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data = request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(TokenObtainPairView):
    serializer_class = LoginJWTSerializer

class AllUsers(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  