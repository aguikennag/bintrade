from django.shortcuts import render
from django.views.generic import ListView,View,RedirectView,TemplateView
from django.views.generic.edit import CreateView,UpdateView
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy,reverse
from urllib.parse import urlparse,urlunparse,urljoin
from .models import Wallet,WithdrawalApplication,Plan,PendingDeposit
from .forms import WithdrawalForm,DepositForm,InvestmentForm
from Users.models import Notification
from myadmin.models import Settings as AdminSetting
from core.mail import Email
from django.utils import timezone
from django.contrib import messages
from django.conf import settings
import datetime


class Deposit(LoginRequiredMixin,View)  :
    template_name = 'deposit.html'
    form_class = DepositForm
    model = PendingDeposit


    def get(self,request,*args,**kwargs) :
        #if self.model.objects.filter(user= request.user,is_active = True).exists():
            #return HttpResponse("You still have a pending deposit, please wait for approval")
        
        form = self.form_class    
        return render(request,self.template_name,locals())

    def post(self,request,*args,**kwargs) :
        #if self.model.objects.filter(user= request.user,is_active = True).exists():
            #return HttpResponse("You still have a pending deposit, please wait for approval")
        form = self.form_class(request.POST,request.FILES)
        user = request.user
        if form.is_valid() :
            form.save(commit=False)
            msg = "Your ${} deposit transaction has been registered and is being processed, you will be notified when processing is completed.".format(
                form.cleaned_data['amount']
            )
            form.instance.user = user
            form.save()
            messages.success(request,msg) 
            #send mail
            ctx = {'text' :  msg , 'name' : user.name}
            mail = Email(send_type="alert")
  
            mail.send_html_email([user.email],ctx = ctx)
            return HttpResponseRedirect(reverse('dashboard'))
        else :
            
            print(form.errors)
            return render(request,self.template_name,locals())    


class Plans(LoginRequiredMixin,ListView) :
    template_name = 'plans.html'
    model = Plan
    context_object_name = "plans"



class Invest(LoginRequiredMixin,View)  :
    template_name = 'invest.html'
    form_class = InvestmentForm
    model = Plan
    plan = None

    def add_referee_earning(self,instance) :
        if instance.user.referee :
            earning = (instance.plan.referral_percentage/100) * instance.amount
            referee_wallet =  instance.user.referee.user_wallet
            referee_wallet.referral_earning += earning
            referee_wallet.save()
            #notify
            msg = "You have been credited with a referral bonus of ${}, for your referral {}.".format(
                earning,
                instance.user.username
            )
            Notification.objects.create(
                user = instance.user.referee,
                message = msg
            )


    def get_context(self) :
        ctx = {}
        user_balance = self.request.user.user_wallet.available_balance   
        #check if balance will permit
        if user_balance < self.plan.min_cost :
            ctx['low_balance'] = True

        #max should be user balance of plan max, which ever is larger
        ctx['max_amount'] = min(self.plan.max_cost or 0.00,user_balance)
        ctx['default_cost'] = min(self.plan.default_cost,user_balance)
        ctx['plan'] = self.plan
        return ctx


    def get(self,request,*args,**kwargs) :
         #check if user has pending deposit
        _slug = kwargs.get('slug',None)
        if not _slug : return HttpResponse("Invalid request")
        try : self.plan = self.model.objects.get(slug =_slug)
        except self.model.DoesNotExist :
            return HttpResponse("Plan you selected does not exist")
        ctx = self.get_context()
        ctx['form'] = self.form_class 
        
        return render(request,self.template_name,ctx)


    def post(self,request,*args,**kwargs) : 
        _slug = kwargs.get('slug',None)
        if not _slug : return HttpResponse("Invalid request")
        try : self.plan = self.model.objects.get(slug =_slug)
        except self.model.DoesNotExist :
            return HttpResponse("Plan you selected does not exist")
        form = self.form_class(user=request.user,data = request.POST)

        if form.is_valid() :
            user = request.user
            form.save(commit=False)
            form.instance.user = user
            investment = form.save()
            self.add_referee_earning(investment)

            if investment.approve_investments() or not user.user_wallet.allow_automatic_investment :
                msg = "You have succesfully subscribed to the {} investment plan (pending processing), with an initial capital of ${}".format(
                    form.instance.plan.name,
                    form.cleaned_data['amount']
                )
            
            else :
                msg = "You have succesfully subscribed to the {} investment plan, with an initial capital of ${}".format(
                    form.instance.plan.name,
                    form.cleaned_data['amount']
                )

                #send mail
                mail = Email(send_type="alert")
                mail.send_investment_mail(investment)
                

            messages.success(request,msg) 
             #send mail
            
            
            return HttpResponseRedirect(reverse('dashboard'))
        else :
        
            ctx = self.get_context()
            ctx['form'] = form

            return render(request,self.template_name,ctx)    






class Withdrawal(LoginRequiredMixin,View)  :  
    model = WithdrawalApplication
    template_name = 'withdraw.html' 
    form_class  = WithdrawalForm

    def withdrawal_allowed(self) :
        try :
            #check general
            general_withdrawal_allowed = AdminSetting.objects.all()[0].enable_withdrawal
            if general_withdrawal_allowed :
                #check for the particular user
                return self.request.user.user_wallet.withdrawal_allowed
            else : return False    
        except : 
            return False
        
    def get(self,request,*args,**kwargs) :  
        withdrawal_allowed = self.withdrawal_allowed()
        return render(request,self.template_name,locals())


    def post(self,request,*args,**kwargs) :
        #to do : on admin approval  deactivate user plan 
        withdrawal_allowed = self.withdrawal_allowed()
        if not  withdrawal_allowed :
            return HttpResponse("Fund withdrawals are not available at the moment, we are working to bring it back ASAP. please check back in a moment")
        
        if not request.user.wallet_address_valid :
            return HttpResponse("""You are yet to enter a valid wallet address, you can't proceed with a withdrawal. Please <a href="{% url 'profile' %}?tab=wallet-address">provide a valid wallet address for payment""")
        
        form = self.form_class(user = request.user,data = request.POST) 
        if form.is_valid() :  
            user = request.user   
            form.save(commit = False)
            form.instance.user = user
            form.save()
            msg = "Your withdrawal application has been submitted for processing,You will be notified once completed."
            messages.success(request,msg)
            Notification.objects.create(user = request.user,message = msg)
            #send mail
            ctx = {'text' :  msg ,'name' : user.name}
            mail = Email(send_type="alert")
            mail.send_html_email([user.email],ctx = ctx)
            return HttpResponseRedirect(reverse('dashboard'))
        
        else :
            return render(request,self.template_name,locals())    
     

