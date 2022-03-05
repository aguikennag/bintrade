from django.views.generic import View,TemplateView,ListView,DetailView
from django.views.generic.edit import  DeleteView,UpdateView
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin,LoginRequiredMixin
from django.shortcuts import render
from .dashboard import AdminBase
from django.http import HttpResponse
from django.urls import reverse
from django.contrib.auth import get_user_model



class FundMember() :
    template_name = "fund-member.html"



class MemberDetail(View)  :
    template_name = 'member-profile.html' 
    model = get_user_model()

    def get(self,request,*args,**kwargs) :
        try :
            user = self.model.objects.get(username = kwargs['username'])
        except :
            return HttpResponse('invalid  request')    
        return render(request,self.template_name,locals())



class MemberEdit(UpdateView) :
    template_name = 'user-update.html'


class EmailMember() :
    template_name = 'create_email.html'






