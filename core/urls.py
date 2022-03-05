from .views import LoginRedirect
from django.urls import path,include

urlpatterns = [
    path('login-redirect',LoginRedirect.as_view(),name = 'login-redirect')
]