from django.urls import path
from .views import TransactionView, AddTransactionView, Summary

urlpatterns = [
    path('transactions/upload/', AddTransactionView.as_view(), name='upload-transaction'),
    path('transactions/view/', TransactionView.as_view(), name='view-transaction'),
    path('summary/', Summary.as_view(), name='summary'),
]
