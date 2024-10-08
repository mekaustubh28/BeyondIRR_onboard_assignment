from django.shortcuts import render
from rest_framework import generics
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Transaction, TransactionSerializer
import pandas as pd
from assets.decode_jwt import decode_jwt
from assets.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from io import BytesIO
import datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# helps to get the current user based on Auth token provided.
def get_current_user(auth_header):
    decoded_token = decode_jwt(auth_header)
    user_id = decoded_token.get('user_id')
    user = User.objects.get(id=user_id)
    return user


class TransactionView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    @swagger_auto_schema(
        operation_summary="Retrieve User Transactions",
        operation_description="""
        This endpoint retrieves a list of transactions for the authenticated user.
        
        **Note:**
        Each product can only have one transaction per day for the authenticated user.
        
        **Authentication:**
        This endpoint requires JWT authentication. Include your token in the `Authorization` header as follows:

        ```
        Authorization: Bearer <your_token_here>
        ```

        **Response:**
        - **200 OK**: Returns a list of transactions for the user.

        **Example Response:**
        ```json
        [
            {
                "id": 1,
                "product": "Product A",
                "asset_class": "Equity",
                "date_of_transaction": "2024-08-18T12:00:00Z",
                "units": 10,
                "amount": 1000
            },
            {
                "id": 2,
                "product": "Product B",
                "asset_class": "Debt",
                "date_of_transaction": "2024-08-18T12:30:00Z",
                "units": 5,
                "amount": 500
            }
        ]
        ```
        """,
    )
    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({"error": "Authorization header missing or invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = get_current_user(auth_header)

        if not user:
            return Response({"error": "User Dont Exist"}, status=status.HTTP_404_NOT_FOUND)

        transactions = Transaction.objects.filter(user=user)
        serializer = self.get_serializer(transactions, many=True)

        return Response({"success": serializer.data}, status=status.HTTP_200_OK)
   

class AddTransactionView(APIView):
    permission_classes = [IsAuthenticated]  
    @swagger_auto_schema(
        operation_summary="Add or Update Transactions",
        operation_description="""
        This endpoint allows authenticated users to add or update if already present, transactions by uploading an Excel file.

        **Note:**
        To Test This Endpoint in Postman follow the steps:
            1. Enter the URL of the API endpoint you want to test in the request URL field.
            2. Make a POST request.
            3. Click on the Body tab below the URL field, choose the form-data option.
            4. Enter 'file' in the key field. 
            5. In the dropdown next to the key field (usually labeled Text), select File. This changes the input type to allow file selection.
            6. Click on the Choose Files button that appears next to the key field.
            7. Navigate to the file you want to upload and select it.
            8. Click on the Send button to submit the request.
            OR
            Directly paste below in the terminal.
        ```bash
        curl --location 'http://127.0.0.1:8000/transactions/upload/' \
        --header 'Authorization: Bearer <your_token_here>' \
        --header 'f;' \
        --form 'file=@"path/to/excel.xlsx"'
        ```
        
        **Authentication:**
        This endpoint requires JWT authentication. Include your token in the `Authorization` header as follows:

        ```
        Authorization: Bearer <your_token_here>
        ```

        **Request Body:**
        - **file**: An Excel file containing transaction data. The file must include the following headers: 'Product', 'Asset Class', 'Date', 'Amount', 'Units'.

        **Response:**
        - **200 OK**: Success message when data is successfully processed.
        - **400 Bad Request**: Error messages for invalid file or data issues.
        """,
    )
    def post(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({"error": "Authorization header missing or invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = get_current_user(auth_header)

        if not user:
            return Response({"error": "User Dont Exist"}, status=status.HTTP_404_NOT_FOUND)


        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            excel_file = BytesIO(file.read())
            df = pd.read_excel(excel_file)
            necessary_headers = ['Product', 'Asset Class', 'Date', 'Amount', 'Units']
            
            for header in necessary_headers:
                if not header in df.columns:
                    return Response({"error": "One or More Necessary Header Missing", "necessary headers": ['Product', 'Asset Class', 'Date', 'Amount', 'Units']}, status=status.HTTP_400_BAD_REQUEST)
                
            records = df.to_dict(orient='records')
            for record in records:
                earlier_transaction = Transaction.objects.filter(user=user, product=record['Product'], date_of_transaction=record['Date'])
                if not earlier_transaction: # if record is not present create one
                    Transaction.objects.create(
                        user=user,
                        product=record['Product'], 
                        asset_class=record['Asset Class'], 
                        date_of_transaction=record['Date'],
                        units=record['Units'],
                        amount=record['Amount']             
                    )
                else: # if record is present update it.
                    earlier_transaction = earlier_transaction[0]
                    earlier_transaction.asset_class = record['Asset Class']
                    earlier_transaction.units = record['Units']
                    earlier_transaction.amount = record['Amount']
                    earlier_transaction.save()

            return Response({"Success": 'Data uploaded for the user.', "user": user.arn_number}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class Summary(APIView):
    permission_classes = [IsAuthenticated]  
    @swagger_auto_schema(
        operation_summary="Get Transaction Summary",
        operation_description="""
        This endpoint provides a summary of transactions grouped by financial year for the authenticated user.

        **Authentication:**
        This endpoint requires JWT authentication. Include your token in the `Authorization` header as follows:

        ```
        Authorization: Bearer <your_token_here>
        ```

        **Response:**
        - **200 OK**: Returns a summary of transactions by financial year.

        **Example Response:**
        ```json
        {
            "FY24-25": {
                "Equity": 1000,
                "Debt": 2000,
                "Alternate": 3000
            },
            "FY23-24": {
                "Equity": 1000,
                "Debt": 2000,
                "Alternate": 0
            },
            ...
        }
        ```
        """,
    )
    def get(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({"error": "Authorization header missing or invalid"}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = get_current_user(auth_header)

        if not user:
            return Response({"error": "User Dont Exist"}, status=status.HTTP_404_NOT_FOUND)

        transactions = Transaction.objects.filter(user=user)
        
        summary = {}
        # logic to create summary sheet
        for t in transactions:
            time = t.date_of_transaction
            timestamp_curr = time.timestamp()
            year = time.year
            
            check_1 = f"{year}-04-01T00:00:00+05:30"
            check_2 = f"{year+1}-04-01T00:00:00+05:30"
            timestamp_1 = datetime.datetime.fromisoformat(check_1).timestamp()
            timestamp_2 = datetime.datetime.fromisoformat(check_2).timestamp()
            #  if date is inside current financial year or previous financial year.
            if timestamp_curr >= timestamp_1 and timestamp_curr < timestamp_2:
                financial_year = f"FY{str(year)[-2:]}-{str(year+1)[-2:]}"
            elif timestamp_curr < timestamp_1:
                financial_year = f"FY{str(year-1)[-2:]}-{str(year)[-2:]}"
            else:
                continue
            
            if financial_year not in summary:
                summary[financial_year] = {
                    "Equity": 0,
                    "Debt": 0,
                    "Alternate": 0
                }
            
            asset = t.asset_class
            if asset == "Equity":
                summary[financial_year]["Equity"] += t.amount
            elif asset == "Debt":
                summary[financial_year]["Debt"] += t.amount
            elif asset == "Alternate":
                summary[financial_year]["Alternate"] += t.amount

        # order was random so sorted in descending order of financial years
        summary = dict(sorted(summary.items(), reverse=True))

        
        return Response({"success": summary}, status=status.HTTP_200_OK)
