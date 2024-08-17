from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
import uuid

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    id = models.UUIDField(default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, default='')
    last_name = models.CharField(max_length=50, default='')
    arn_number = models.IntegerField(unique=True, primary_key=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'arn_number']

    def __str__(self):
        return self.email


class LogRequests(models.Model):    
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    url = models.CharField(editable=False, max_length=1000)
    method = models.CharField(max_length=10, editable=False)
    request_payload = models.JSONField(editable=False)
    response_payload = models.JSONField(null=True, blank=True, editable=False)
    status_code = models.IntegerField(editable=False)
    timestamp = models.DateTimeField(auto_now_add=True, editable=False)
    success = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return f"{self.timestamp} - {self.status_code}"