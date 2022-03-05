from django.shortcuts import render
from django.views.generic import View,RedirectView
from django.http import HttpResponseRedirect
from django.urls import reverse

class LoginRedirect(RedirectView) :
    def get(self,request,*args,**kwargs) :
        try :
            if request.user.is_admin :
                return HttpResponseRedirect(reverse('admin-dashboard'))
            else : 
                return HttpResponseRedirect(reverse('dashboard')) 
        except :
            return HttpResponseRedirect(reverse('dashboard'))      