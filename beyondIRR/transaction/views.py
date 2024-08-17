from django.shortcuts import render
from rest_framework import generics
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import Transaction, TransactionSerializer
import pandas as pd
from assets.decode_jwt import decode_jwt
from assets.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from io import BytesIO

# Create your views here.

def get_current_user(auth_header):
    decoded_token = decode_jwt(auth_header)
    user_id = decoded_token.get('user_id')
    user = User.objects.get(id=user_id)
    return user


class TransactionView(generics.ListAPIView):
    serializer_class = TransactionSerializer

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
            records = df.to_dict(orient='records')
            for record in records:
                earlier_transaction = Transaction.objects.filter(user=user, product=record['Product'], date_of_transaction=record['Date'])
                if not earlier_transaction:
                    Transaction.objects.create(
                        user=user,
                        product=record['Product'], 
                        asset_class=record['Asset Class'], 
                        date_of_transaction=record['Date'],
                        units=record['Units'],
                        amount=record['Amount']             
                    )
                else:
                    earlier_transaction = earlier_transaction[0]
                    earlier_transaction.asset_class = record['Asset Class']
                    earlier_transaction.units = record['Units']
                    earlier_transaction.amount = record['Amount']
                    earlier_transaction.save()

            return Response({"Success": 'Data uploaded for the user.', "user": user.arn_number}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
      