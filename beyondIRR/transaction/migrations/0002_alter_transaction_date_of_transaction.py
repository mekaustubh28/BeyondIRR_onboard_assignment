# Generated by Django 5.1 on 2024-08-17 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transaction', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='date_of_transaction',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
