
from django.shortcuts import render
from django.views.generic import ListView,View,RedirectView,TemplateView
from django.views.generic.edit import CreateView,UpdateView
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy,reverse
from django.forms.models import model_to_dict
from django.http import HttpResponseRedirect
from .forms import ProfileForm, VerifyEmailForm,WalletForm

from core.mail import Email
from core.forms import OtpForm



class Profile(LoginRequiredMixin,UpdateView) :
    template_name = 'profile.html'
    model = get_user_model()
    form_class = ProfileForm
    wallet_form = WalletForm
    verify_email_form  = VerifyEmailForm
    otp_form  = OtpForm

    
    def get_success_url(self):
        messages.success(self.request,"Your profile was updated successfully.") 
        return reverse('dashboard')
    
    def get_object(self) :
        return self.request.user

    def get_context_data(self, **kwargs) :
        ctx = super(Profile,self).get_context_data(**kwargs)  
        ctx['wallet_form'] = self.wallet_form(initial = model_to_dict(self.request.user))
        ctx['verify_email_form'] = self.verify_email_form(initial = model_to_dict(self.request.user))
        ctx['otp_form'] = self.otp_form
        ctx['tab']  =  self.request.GET.get('tab','personal-data')
        return ctx




class WalletUpdate(LoginRequiredMixin,UpdateView) :
    template_name = 'profile.html'
    model = get_user_model()
    form_class = WalletForm
    
    def get_success_url(self):
        messages.success(self.request,"Your wallet details was updated successfully.") 
        return reverse('dashboard')
    
    def get_object(self) :
        return self.request.user


class VerifyEmail(LoginRequiredMixin,View) :
    template_name = 'verify.html'
    form_class = VerifyEmailForm
    otp_form = OtpForm
    
    #remember to ask for password in the verify form
    #we should have a passsword verify form


    def post(self,request,*args,**kwargs) :
    
        form = self.form_class(data=request.POST)
        otp_form = self.otp_form(data = request.POST,user = request.user)
        
        
        if otp_form.is_valid() :
            if form.is_valid() :
                #if email is edited
                new_email = form.cleaned_data['email']
                request.user.email = new_email
                request.user.email_verified = True
                request.user.save()
            
            else :
                ctx = {
                    'form' : form , 'otp_form' : otp_form,
                    "form_title" : "Email Verification" ,
                    "target"  : "mail"
                    }
                return render(request,self.template_name,ctx)         
        
        else :
            ctx = {'form' : form , 'otp_form' : otp_form,
            "form_title" : "Email Verification" ,
            "target"  : "mail"
            }
            return render(request,self.template_name,ctx) 
        #success 
        #send message 
        msg = "Your email has been verified successfully ."
    
        if request.user.email_verified :
            mail = Email(send_type='support')  
            mail.send_email([new_email],'Email Verified successfully',msg)   

        return HttpResponseRedirect(reverse("profile",args = [request.user]))     

    
