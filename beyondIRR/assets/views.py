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
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class SignUp(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        operation_summary="Sign Up a New User",
        operation_description="""
        This endpoint allows users to sign up by providing their details. The request should include the user's information, 
        including their email, password, ARN number, name.
        **Note:**
        Before Signing up Api check for email and arn number validity at from AMFI website.
        
        **Authentication:**  
        This endpoint does not require authentication.

        **Request Body:**
        - `email`: Email address of the user (string)
        - `password`: Password for the user (string)
        - `arn_number`: ARN number of the user (integer). Don't add starting zeros Eg. If arn_number = 0069 type 69.
        - `first_name`: First Name of the user (string)
        - `last_name`: Last Name of the user (Optional) (string)

        **Response:**
        - **201 Created**: User created successfully. Returns a message and the user's data.
        - **400 Bad Request**: Validation error. Returns the error message and data.
        - **404 Not Found**: If the ARN number or email does not match the AMFI database.

        **Example Request:**
        ```json
        {
            "email": "user@example.com",
            "password": "password123",
            "arn_number": 12345,
            "first_name": "User",
            "last_name": "doe"
        }
        ```
        """,
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
                'arn_number': openapi.Schema(type=openapi.TYPE_INTEGER, description='ARN number'),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description='First Name'),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description='Last Name'),
            },
            required=['email', 'password', 'arn_number', 'first_name']
        ),
        responses={
            201: openapi.Response('User created successfully', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'message': openapi.Schema(type=openapi.TYPE_STRING, description='Success message'),
                    'data': openapi.Schema(type=openapi.TYPE_OBJECT, description='User data')
                }
            )),
            400: openapi.Response('Bad request', openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    'error': openapi.Schema(type=openapi.TYPE_STRING, description='Error message')
                }
            )),
        }

    )
    @log_request(record_success=True)
    def post(self, request, *args, **kwargs):
        """
        Retrieve a list of items.
        This is a detailed description of what this API endpoint does.
        """
        serializer = UserSerializer(data=request.data)
   
        res = check_arn(request.data['arn_number'])
        
        if serializer.is_valid():
            try:
                if 'amfi_arn_number' in res:
                    if not res['amfi_email'] == request.data['email']:
                        del request.data['password']
                        response = Response({"error": "Given Email dont match AMFI Database. Please verify at https://www.amfiindia.com/locate-your-nearest-mutual-fund-distributor-details.", "data": request.data, "status":status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)
                        return response
                else:
                    del request.data['password']
                    return Response({"error": res, "data": request.data, "status":status.HTTP_404_NOT_FOUND}, status=status.HTTP_404_NOT_FOUND)

                serializer.save()
                
                del request.data['password']
                return Response({"message": "User created successfully", "data": request.data, "status":status.HTTP_201_CREATED}, status=status.HTTP_201_CREATED)
            except ValidationError as e:
                
                del request.data['password']
                return Response({"error": str(e), "data": request.data, "status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
            
        del request.data['password']
        return Response({"error": serializer.errors, "data": request.data, "status":status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)


class Login(TokenObtainPairView):
    serializer_class = LoginJWTSerializer
    @swagger_auto_schema(
        operation_summary="Obtain JWT Token",
        operation_description="""
        This endpoint allows users to log in by providing their credentials and obtain a JWT token.
        
        **Authentication:**  
        This endpoint does not require authentication.
        
        **Request Body:**
        - `email`: The email address of the user (string)
        - `password`: The password for the user (string)

        **Response:**
        - **200 OK**: Returns the JWT access and refresh tokens.
        - **401 Unauthorized**: Invalid credentials.

        **Example Request:**
        ```json
        {
            "email": "user@example.com",
            "password": "password123"
        }
        ```
        """,
    )
    def post(self, request, *args, **kwargs):
        """
        Obtain JWT Token.
        """
        return super().post(request, *args, **kwargs)

class AllUsers(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  
    
    @swagger_auto_schema(
        operation_summary="Retrieve All Users",
        operation_description="""
        This endpoint retrieves a list of all users in the Database. It is accessible only to authenticated admin users.
        
        **Authentication:**  
        This endpoint requires JWT authentication. Include your token in the `Authorization` header as follows:

        ```
        Authorization: Bearer <your_token_here>
        ```

        **Response:**
        - **200 OK**: Returns a list of users.
        
        **Example Response:**
        ```json
        [
            {
                "id": 1,
                "email": "user1@example.com",
                "arn_number": "5643",
                "first_name": "user1",
                "last_name": "surname"
                ...
            },
            {
                "id": 2,
                "email": "user2@example.com",
                "arn_number": "1234",
                "first_name": "user2"
                ...
            }
            ...
        ]
        ```
        """,
        
    )
    def get(self, request, *args, **kwargs):
        """
        Return All users in the database.
        """
        return super().get(request, *args, **kwargs)

class CurrentUser(APIView):
    permission_classes = [IsAuthenticated]  
    @swagger_auto_schema(
        operation_summary="Retrieve Current User",
        operation_description="""
        This endpoint retrieves the details of the currently authenticated user.
        
        **Authentication:**  
        This endpoint requires JWT authentication. Include your token in the `Authorization` header as follows:

        ```
        Authorization: Bearer <your_token_here>
        ```

        **Response:**
        - **200 OK**: Returns the user details.
        - **401 Unauthorized**: Invalid or missing JWT token.

        **Example Response:**
        ```json
        {
            "message": "Success",
            "user_email": "user@example.com"
            "user_arn_number: "12345",
        }
        ```
        """,
    )
    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({"error": "Authorization header missing or invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            decoded_token = decode_jwt(auth_header)
            user_id = decoded_token.get('user_id')
            
            user = User.objects.get(id=user_id)
            
            return Response({"message": "Success", "user_email": user.email, "user_arn_number": user.arn_number}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_401_UNAUTHORIZED)

class LogView(generics.ListAPIView):
    queryset = LogRequests.objects.all()
    serializer_class = LogRequestsSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]  
    
    @swagger_auto_schema(
        operation_summary="Retrieve Log Requests",
        operation_description="""
        This endpoint retrieves a list of all log requests while interating with the signup endpoint. It is accessible only to authenticated admin users.
        
        **Authentication:**  
        This endpoint requires JWT authentication. Include your token in the `Authorization` header as follows:

        ```
        Authorization: Bearer <your_token_here>
        ```

        **Response:**
        - **200 OK**: Returns a list of log requests.

        """,
    )
    def get(self, request, *args, **kwargs):
        """
        Return Logs for every interation with Signup Endpoint.
        """
        return super().get(request, *args, **kwargs)
