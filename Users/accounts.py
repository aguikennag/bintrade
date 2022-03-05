from django.urls import reverse_lazy,reverse
from django.shortcuts import render
from django.views.generic import CreateView,View,RedirectView
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from wallet.models import Wallet
from myadmin.models import MyAdmin
from core.notification import Notification
from core.mail import Email
from .models import  User
from .forms import UserCreateForm

class Register(CreateView) :
    template_name = 'register.html'
    model = User
    form_class = UserCreateForm
    success_url = reverse_lazy('login')

    def get(self,request,*args,**kwargs) :
        initials = {}

        if 'ref_id' in request.GET :     
            ref_id = request.GET['ref_id']  
            try : 
                ref_id = int(ref_id)  #cleaning
                initials['referral_id'] = ref_id
            except : 
                return HttpResponse("Invalid request format")
            
        form = self.form_class(initial=initials)   
        return render(request,self.template_name,locals())


    def auto_create_wallet(self,user) :
        Wallet.objects.create(user = user)
        return

    def add_ref_earning(self) :
        #add referral earning
        """ref_id = form.cleaned_data.get('ref_id',None)
        if ref_id :
            #add for user
            try : 
                referer = User.objects.get(referral_id  = ref_id)
                referer.referals.add(user)
                referer.user_wallet.referral_earning += ref_bonus
                referer.user_wallet.save()
                #notify user of bonus
                msg = "{} just registered with you referal id,you just got a referral bonus of {}".format(user.username,ref_bonus)
                Notification.objects.create(user = referer,message = msg)
            except : 
                pass"""    

    def post(self,request,*args,**kwargs) :
        my_reg_id = ""
        my_ref_id = ""
        form = self.form_class(request.POST)
        if form.is_valid() :
            ref_bonus  = 10 #in $dollars
            user  = form.save()
            self.auto_create_wallet(user)
        
            #send welcome email
            mail = Email()    
            try : mail.welcome_email(user) 
            except : pass
        return HttpResponseRedirect(self.success_url)


class LoginRedirect(LoginRequiredMixin,RedirectView) :
    def get(self,request,*args,**kwargs) :
        if request.user.is_admin :
            return HttpResponseRedirect((reverse('admin-dashboard')))
        else :
            return HttpResponseRedirect((reverse('dashboard'))) 



    