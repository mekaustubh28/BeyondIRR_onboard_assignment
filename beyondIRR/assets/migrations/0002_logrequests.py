# Generated by Django 5.1 on 2024-08-17 12:42

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogRequests',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('url', models.CharField(editable=False, max_length=1000)),
                ('method', models.CharField(editable=False, max_length=10)),
                ('request_payload', models.JSONField(editable=False)),
                ('response_payload', models.JSONField(blank=True, editable=False, null=True)),
                ('status_code', models.IntegerField(editable=False)),
                ('timestamp', models.CharField(editable=False, max_length=100)),
                ('success', models.BooleanField(default=False, editable=False)),
            ],
        ),
    ]
