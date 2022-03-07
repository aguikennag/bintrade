from django.urls import path,include
from .pages import Index,TOS,About,Contact,Faq


urlpatterns = [
    path('',Index.as_view(),name = 'index'),
    path('about/',About.as_view(),name = 'about-us'),
    path('contact/',Contact.as_view(),name = 'contact'),
    path('FAQ/',Faq.as_view(),name='faq'),
    path('terms-of-service/',TOS.as_view(),name = 'legal'),    
    
]