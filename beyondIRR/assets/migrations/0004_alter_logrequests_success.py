# Generated by Django 5.1 on 2024-08-17 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0003_alter_logrequests_success_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logrequests',
            name='success',
            field=models.BooleanField(editable=False, null=True),
        ),
    ]
