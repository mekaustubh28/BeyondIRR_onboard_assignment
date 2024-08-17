from django.db import models
from assets.models import User
from rest_framework import serializers
import uuid


# Create your models here.
ASSET_CHOICES = (
    ("EQUITY","Equity"),
    ("DEBT", "Debt"),
    ("ALTERNATE", "Alternate")
)



class Transaction(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.CharField(default='', max_length=100)
    asset_class = models.CharField(default='', choices=ASSET_CHOICES, max_length=100)
    date_of_transaction = models.DateTimeField()
    units = models.DecimalField(default=0, decimal_places=4, max_digits=10)
    amount = models.DecimalField(default=0, decimal_places=4, max_digits=10)

    def __str__(self):
        return f"{self.id}"
    

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'product', 'asset_class', 'date_of_transaction', 'units', 'amount']