from django.urls import path
from .views import TransactionView, AddTransactionView

urlpatterns = [
    path('transactions/upload/', AddTransactionView.as_view(), name='upload-transaction'),
    path('transactions/view/', TransactionView.as_view(), name='view-transaction'),
]
