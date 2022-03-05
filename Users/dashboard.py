from django.shortcuts import render
from django.views.generic import ListView,View,RedirectView,TemplateView
from django.views.generic.edit import CreateView,UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.forms.models import model_to_dict
from wallet.models import Wallet,WithdrawalApplication
from .forms import ProfileUpdateForm


class Dashboard(LoginRequiredMixin,TemplateView) :
    template_name = 'dashboard.html'

    def get_context_data(self,*args,**kwargs) :
        ctx = super(Dashboard,self).get_context_data(*args,**kwargs)  
        if 'wthl' in self.request.GET : 
            ctx['redirect_message'] = "Your withdrawal request was successful"
        elif 'dpt' in self.request.GET :
            ctx['redirect_message'] = "Your deposit has been acknowledged,awaiting approval." 
        
        init = self.request.user.username[0] 
        ctx['initial'] = init.upper()
        #ctx['pending_deposit'] = request.user.
        return ctx

    def get(self,request,*args,**kwargs)   :
        if request.user.user_wallet.plan_is_due :
            request.user.user_wallet.on_plan_complete()
        return render(request,self.template_name,{})    



class Profile(LoginRequiredMixin,UpdateView) :
    template_name = 'profile.html'
    model = get_user_model()
    form_class = ProfileUpdateForm
    success_url = reverse_lazy('dashboard')
    
    def get_object(self) :
        return self.request.user

    def get(self,request,*args,**kwargs) :
        form = self.form_class(initial = model_to_dict(request.user))
        return render(request,self.template_name,locals())

