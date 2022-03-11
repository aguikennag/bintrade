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


class Members(AdminBase,View) :
    template_name = 'members.html'
    model = get_user_model()

    def get(self,request,*args,**kwargs) :
        members = self.model.objects.exclude(
            user_wallet__isnull = True
        ).order_by('-name','-username')
        return render(request,self.template_name,locals())



class MemberDetail(DetailView)  :
    template_name = 'member-profile.html' 
    model = get_user_model()
    context_object_name = "member"


class MemberEdit(UpdateView) :
    template_name = 'user-update.html'


class EmailMember() :
    template_name = 'create_email.html'






