from django.urls import path
from .views import SignUp, Login, AllUsers, LogView

urlpatterns = [
    path('signup/', SignUp.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('users/', AllUsers.as_view(), name='users'),
    path('logs/', LogView.as_view(), name='log-list'),
]
