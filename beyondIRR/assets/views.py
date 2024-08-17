from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import User, LogRequests
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, LoginJWTSerializer, LogRequestsSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.exceptions import ValidationError
from .decorator import log_request

class SignUp(APIView):
    permission_classes = [AllowAny]

    @log_request(record_success=False)
    def post(self, request, *args, **kwargs):
        
        serializer = UserSerializer(data=request.data)
        
        
        if serializer.is_valid():
            try:
                serializer.save()
                del request.data['password']
                return Response({"message": "User created successfully", "data": request.data, "status": status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                
                del request.data['password']
                return Response({"error": str(e), "data": request.data, "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            
        del request.data['password']
        return Response({"error": serializer.errors, "data": request.data, "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

class Login(TokenObtainPairView):
    serializer_class = LoginJWTSerializer

class AllUsers(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]  


class LogView(generics.ListAPIView):
    queryset = LogRequests.objects.all()
    serializer_class = LogRequestsSerializer
    permission_classes = [AllowAny]  
