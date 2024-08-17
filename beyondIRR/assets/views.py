from django.shortcuts import render
from rest_framework import status, generics
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .models import User, LogRequests
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import UserSerializer, LoginJWTSerializer, LogRequestsSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.exceptions import ValidationError
from .decorator import log_request
from .decode_jwt import decode_jwt
from .arn_verification import check_arn

class SignUp(APIView):
    permission_classes = [AllowAny]

    @log_request(record_success=False)
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        res = check_arn(request.data['arn_number'])
        
        
        if serializer.is_valid():
            try:

                if 'amfi_arn_number' in res:
                    if not res['amfi_email'] == request.data['email']:
                        del request.data['password']
                        return Response({"error": "Given Email dont match AMFI Database. Please verify at https://www.amfiindia.com/locate-your-nearest-mutual-fund-distributor-details.", "data": request.data, "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
                else:
                    del request.data['password']
                    return Response({"error": res, "data": request.data, "status": status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

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
    permission_classes = [IsAuthenticated, IsAdminUser]  

class CurrentUser(APIView):
    permission_classes = [IsAuthenticated]  

    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({"error": "Authorization header missing or invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            decoded_token = decode_jwt(auth_header)
            user_id = decoded_token.get('user_id')
            
            user = User.objects.get(id=user_id)
            
            return Response({"message": "Success", "user_id": user.arn_number}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

class LogView(generics.ListAPIView):
    queryset = LogRequests.objects.all()
    serializer_class = LogRequestsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  
