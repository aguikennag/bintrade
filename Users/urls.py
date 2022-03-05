from  django.urls import path,include
from .views import Subscribe
from .accounts import Register,LoginRedirect
from .dashboard import Dashboard,Profile

urlpatterns = [
    path('subscribe/',Subscribe.as_view(),name = 'subscribe'),
    path('register/',Register.as_view(),name = 'register'),
    path('dashboard/',Dashboard.as_view(),name = 'dashboard'),
    path('profile/',Profile.as_view(),name = 'profile'),

    path('login-redirect/',LoginRedirect.as_view(),name="login-redirect")


    #path('profile/',Profile.as_view(),name = 'register'),
    

]